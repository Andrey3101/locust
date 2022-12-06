
import json
import logging
import datetime
from random import randint, choice
from hashlib import sha1
from nko import *

from management import ManagementApi

loger = logging.getLogger("locust_setup")
loger.setLevel(logging.INFO)

configfile = open('settings.json', 'r')
settings = json.loads(configfile.read())

management_api_url = settings['management_api_url']
nko_api_url = settings['nko_url']

login = settings['login']
passwd = settings['passwd']
region_id = settings['region_id']

management_api = ManagementApi(management_api_url)
management_token = (management_api.authorize(login,passwd)).text
nko_api = NKOApi(nko_api_url)

def check_oiv(region):
    # проверка соц.учреждения при отсутствии создание
    oiv_id = None
    post_data = json.dumps({"regionIds":[region_id]})
    oivs = management_api.get_oiv(management_token, post_data)
    assert oivs.status_code == 200, oivs.text
    oivs = json.loads(oivs.text.encode('utf-8').decode('utf-8-sig'))
    for oiv in oivs['data']:
        if oiv['typeId'] == 1 and oiv['regionId'] == int(region):
            oiv_id = oiv['id']
            loger.info('Найдено соц.учредление с id {0}'.format(oiv_id))
            break
    if oiv_id == None:
        new_oiv = json.dumps({"name":"ОИВ"+str(region_id),"typeId":1,"regionId":region})
        oiv = management_api.create_oiv(management_token, new_oiv)
        assert oiv.status_code == 200, oiv.text
        oiv = json.loads(oiv.text.encode('utf-8').decode('utf-8-sig'))
        oiv_id = oiv['id']
        loger.info('Создано соц.учредление с id {0}'.format(oiv_id))
    return oiv_id

def check_benefittype(region):
    # проверка категории льгот при отсутствии создание
    benefittype = None
    region = int(region)
    post_data = {"regionIds":[region]}
    benefittypes = management_api.get_benefittype(management_token, json.dumps(post_data))
    assert benefittypes.status_code == 200, benefittypes.text
    benefittypes = json.loads(benefittypes.text.encode('utf-8').decode('utf-8-sig'))
    for benefitt in benefittypes['data']:
        if benefitt['regionId'] == region:
            benefittype = benefitt['id']
            loger.info('Получена категория льготы с id {0}'.format(benefittype))
            break
    if benefittype == None:
        last_code = management_api.get_benefittype(management_token, json.dumps({"page":1,"pageSize":1,"column":"Code","direction":2,"regionIds":[region]}))
        assert last_code.status_code == 200, last_code.text
        last_code = json.loads(last_code.text.encode('utf-8').decode('utf-8-sig'))
        try:
            last_code = int(last_code['data'][0]['code'])
        except IndexError or KeyError:
            last_code = 0
        new_benefittype = {"code":str(last_code+1),"name":"Оплата товаров с соц. счета для НТ","regionId":region,"description":"Категория льготы для нагрузочного тестирования"}
        new_benefittype = management_api.add_benefittype(management_token, json.dumps(new_benefittype))
        assert new_benefittype.status_code == 200, new_benefittype.text
        new_benefittype = json.loads(new_benefittype.text.encode('utf-8').decode('utf-8-sig'))
        benefittype = new_benefittype['id']
        loger.info('Создано категория льготы с id {0}'.format(benefittype))
    return benefittype

def check_social_program(region, benefitTypeId, oiv_id):
    # проверка соц.программы при отсутствии создание
    social_program_id = None
    post_data = {"executiveAuthorityIds":[oiv_id],"regionIds":[region]}
    social_programs = management_api.get_social_programs(management_token, json.dumps(post_data))
    assert social_programs.status_code == 200, social_programs.text
    social_programs = json.loads(social_programs.text.encode('utf-8').decode('utf-8-sig'))
    for social_prog in social_programs['data']:
        if social_prog['regionId'] == int(region):
            social_program_id = social_prog['id']
            social_program_code = social_prog['code']
            loger.info('Получена соц.программа с id {0} с кодом {1}'.format(social_program_id, social_program_code))
            break
    if social_program_id == None:
        date = (datetime.datetime.now()-datetime.timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S")
        new_social_program = json.dumps({"name":"Социальная программа Locust","dateFrom":date,"dateTo":None,"typeId":1,"executiveAuthorityId":oiv_id,"regionId":region,"benefitTypeIds":[benefitTypeId],"description":"Социальная программа для нагрузочного тестирования Locust"})
        new_social_program = management_api.creat_social_program(management_token, new_social_program)
        assert new_social_program.status_code == 200, new_social_program.text
        new_social_program = json.loads(new_social_program.text.encode('utf-8').decode('utf-8-sig'))
        social_program_id = new_social_program['id']
        create_soc_prog = management_api.get_social_program_by_id(management_token,social_program_id)
        assert create_soc_prog.status_code == 200, create_soc_prog.text
        create_soc_prog = json.loads(create_soc_prog.text.encode('utf-8').decode('utf-8-sig'))
        social_program_code = create_soc_prog['code']
        loger.info('Создана соц.программа с id {0} с кодом {1}'.format(social_program_id, social_program_code))
    return social_program_id, social_program_code

def check_TSP(region, social_program):
    # проверка торгового предприятия (тсп) при отсутствии создание
    tsp_id = None
    post_data = ({"regionIds":[region_id]})
    tsps = management_api.get_tsp(management_token, json.dumps(post_data))
    assert tsps.status_code == 200, tsps.text
    tsps = json.loads(tsps.text.encode('utf-8').decode('utf-8-sig'))
    for test_tsp in tsps['data']:
        if social_program in test_tsp['socialProgramIds'] and test_tsp['regionId'] == int(region):
            tsp_id = test_tsp['id']
            tsp_code = test_tsp['code']
            loger.info('Получено торговое предприятие с id {0} с кодом {1}'.format(tsp_id, tsp_code))
            break
    if tsp_id == None:
        # Насчет кода надо подумать, возможно придется его генерить или брать из сформированного файла
        last_code = management_api.get_tsp(management_token, json.dumps({"page":1,"pageSize":1,"column":"Code","direction":2}))
        assert last_code.status_code == 200, last_code.text
        # last_code = json.loads(last_code.text.encode('utf-8').decode('utf-8-sig'))
        try:
            last_code = str(int((json.loads(last_code.text.encode('utf-8').decode('utf-8-sig')))['data'][0]['code'])+1).zfill(5)
        except IndexError or KeyError or AttributeError:
            last_code = '1'
        new_tsp = json.dumps({"name": "ТСП Locust", "typeId":1, "code": last_code,"legalName": "Locust-TSP", "inn": "1234567890", "legalAddress": "Adress", "phone": "+79999999999" , "regionId": int(region), "socialProgramIds": [social_program]})
        new_tsp = management_api.create_tsp(management_token, new_tsp)
        assert new_tsp.status_code == 200, new_tsp.text
        new_tsp = json.loads(new_tsp.text.encode('utf-8').decode('utf-8-sig'))
        tsp_id = new_tsp['id']
        tsp_code = new_tsp['code']
        loger.info('Создано торговое предприятие с id {0} с кодом {1}'.format(tsp_id, tsp_code))
    return tsp_id, tsp_code

def check_shop(tsp_id):
    # проверка магазина при отсутствии создание
    shop_id = None
    post_data = ({"merchantIds": [tsp_id]})
    shop = management_api.get_shopNode(management_token, json.dumps(post_data))
    assert shop.status_code == 200, shop.text
    shop = json.loads(shop.text.encode('utf-8').decode('utf-8-sig'))
    for test_shop in shop['data']:
        if test_shop['merchantId'] == tsp_id:
            shop_id = test_shop['id']
            Shop_code = test_shop['code']
            loger.info('Получен магазин с id {0} с кодом {1}'.format(shop_id, Shop_code))
            break
    if shop_id == None:
        get_code = {"merchantIds":[1],"column":"Code","direction":2}
        last_code = management_api.get_shopNode(management_token, json.dumps(get_code))
        assert last_code.status_code == 200, last_code.text
        try:
            last_code = str(int((json.loads(last_code.text.encode('utf-8').decode('utf-8-sig')))['data'][0]['code'])+1).zfill(5)
        except IndexError:
            last_code = '00001'
        new_shop = json.dumps({"name": "Тестовый магазин Locust", "code": last_code, "address": "г. Санкт-петербург, Пионерская улица 45", "phone": "88005555555", "merchantId": tsp_id})
        new_shop = management_api.create_shop(management_token, new_shop)
        assert new_shop.status_code == 200, new_shop.text
        new_shop = json.loads(new_shop.text.encode('utf-8').decode('utf-8-sig'))
        shop_id = new_shop['id']
        Shop_code = new_shop['code']
        loger.info('Создан магазин с id {0} с кодом {1}'.format(shop_id, Shop_code))
    return shop_id, Shop_code

def check_terminal(shop_id, tsp_id, count):
    # проверка кассы у магазина при отсутствии создание
    terminalsNumber = []
    post_data = {"merchantIds":[tsp_id],"shopIds":[shop_id]}
    terminals = management_api.get_terminalNode(management_token, json.dumps(post_data))
    assert terminals.status_code == 200, terminals.text
    terminals = json.loads(terminals.text.encode('utf-8').decode('utf-8-sig'))
    for term in terminals['data']:
        if tsp_id == term['merchantId'] and shop_id == term['shopId']:
            terminalsNumber.append(term['number'])
            loger.info('Получен терминал с номером {0} магазина c id {1}, всего {2}'.format(term['number'], shop_id, len(terminalsNumber)))
    if len(terminalsNumber) <= count:
        for term in range(count-len(terminalsNumber)):
            numbers = randint(1000000000,9999999999)
            while str(numbers) in terminalsNumber:
                numbers = randint(1000000000,9999999999)
            new_term = json.dumps({"number": numbers, "merchantId": tsp_id, "shopId": shop_id})
            new_term = management_api.create_terminal(management_token, new_term)
            assert new_term.status_code == 200, new_term.text
            new_term = json.loads(new_term.text.encode('utf-8').decode('utf-8-sig'))
            terminalsNumber.append(new_term['number'])
            loger.info('Создана касса (терминал) c номером {2} для магазина c id {0}, всего терминалов у магазина {1}'.format(shop_id, len(terminalsNumber), new_term['number']))
    return terminalsNumber

def check_product_category(tsp_id):
    # проверка наличия категории продутов при отсутствии создание
    product_category = []
    post_data = {"merchantIds": [tsp_id]}
    category_product = management_api.get_product_category(management_token, json.dumps(post_data))
    assert category_product.status_code == 200, category_product.text
    category_product = json.loads(category_product.text.encode('utf-8').decode('utf-8-sig'))
    for cat_product in category_product['data']:
        if tsp_id == cat_product['merchantId']:
            product_category.append(cat_product['id'])
            loger.info('Получены категории товаров торгового предприятия c id {0}, всего {1}'.format(tsp_id, len(product_category)))
    if product_category == []:
        code_prod_cat = ''.join(choice('1234567890') for i in range(10))
        get_prod_cat = {"name": "Тестовая категория", "code": code_prod_cat, "merchantId": tsp_id}
        prod_cat = management_api.create_product_catagory(management_token, json.dumps(get_prod_cat))
        assert prod_cat.status_code == 200, prod_cat.text
        prod_cat = json.loads(prod_cat.text.encode('utf-8').decode('utf-8-sig'))
        product_category.append(prod_cat['id'])
        loger.info('Создана категория товаров {0} для торгового предприятия c id {1}'.format(prod_cat['id'], tsp_id))
    return product_category

def check_catalog(tsp_id, soc_prog, count_product_in_catalog, product_category, oiv_id):
    # проверка соц.каталога продуктов при отсутствии создание
    products_in_catalog, products_in_catalog_get = [], []
    catalog_id = None
    post_data = {"merchantIds":[tsp_id],"socialProgramIds":[soc_prog]}
    catalogs = management_api.get_catalogs(management_token, json.dumps(post_data))
    assert catalogs.status_code == 200, catalogs.text
    catalogs = json.loads(catalogs.text.encode('utf-8').decode('utf-8-sig'))
    for catalog in catalogs['data']:
        if tsp_id == catalog['merchantId'] and soc_prog == catalog['socialProgramId'] and catalog['statusId'] == 3 and catalog['executiveAuthorityId'] == oiv_id:
            catalog_id = catalog['id']
            products_get = {"productCatalogId":catalog_id}
            products = management_api.get_product_catalog_product(management_token,json.dumps(products_get))
            assert products.status_code == 200, products.text
            products = (json.loads(products.text.encode('utf-8').decode('utf-8-sig')))['data']
            if len(products) >= count_product_in_catalog:
                products_in_catalog_get = products
                loger.info('Получен каталог соц.пргораммы с id {0}, id каталога {1}, кол-во продуктов в нём {2}'.format(soc_prog, catalog_id ,len(products)))
                break
    if products_in_catalog_get == []:
        loger.info(('В каталоге нет товаров или кол-во товаров менее ожидаемого ({0}), проиходит создание, наполнение и подтверждение нового каталога').format(count_product_in_catalog))
        catalog_id = None
        date = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
        cr_catalog = {"merchantId": tsp_id, "socialProgramId": soc_prog, "statusId": 1, "dateFrom": date, "executiveAuthorityId": oiv_id, "typeId": 1}
        post_catalog = management_api.create_catalog(management_token, json.dumps(cr_catalog))
        assert post_catalog.status_code == 200, post_catalog.text
        post_catalog = json.loads(post_catalog.text.encode('utf-8').decode('utf-8-sig'))
        assert post_catalog['statusId'] == 1
        catalog_id = post_catalog['id']
        loger.info('Создан каталог с id {0}'.format(catalog_id))
        for product in range(count_product_in_catalog):
            code_product = ''.join(choice('123456') for i in range(6))
            price = ''.join(choice('1234567890') for i in range(3))
            cr_product_post = {"name": "Товар НГ Locust "+code_product, "merchantId": tsp_id, "categoryId": product_category[0], "unitTypeId": 1 , "price" :  price, "productCatalogId": catalog_id, "code": code_product} # Отсутствует проверка категории, вытянуть id каталога
            cr_product = management_api.create_product(management_token, json.dumps(cr_product_post))
            assert cr_product.status_code == 200, cr_product.text
            loger.info('Создан продукт {1} с порядковым номером {0} из {2}'.format(product, cr_product_post['name'], count_product_in_catalog))
            cr_product = (json.loads(cr_product.text.encode('utf-8').decode('utf-8-sig')))
        products_get = {"productCatalogId":catalog_id}
        products = management_api.get_product_catalog_product(management_token,json.dumps(products_get))
        assert products.status_code == 200, products.text
        products = (json.loads(products.text.encode('utf-8').decode('utf-8-sig')))['data']
        if len(products) >= count_product_in_catalog:
            loger.info('Создано и добавлено {1} продукта(ов) в каталог с id {0}'.format(catalog_id, len(products)))
            products_in_catalog_get = products
        matching_catalog = {"id": catalog_id}
        matching = management_api.matching_catalog(management_token, json.dumps(matching_catalog),full=False)
        assert matching.status_code == 200, matching.text
        fullmatching = management_api.matching_catalog(management_token, json.dumps(matching_catalog),full=True)
        assert fullmatching.status_code == 200, fullmatching.text
    for product in products_in_catalog_get:
        products_in_catalog.append({'PdctCd': product['code'], 'UnitOfMeasr': 'PIEC', 'PdctQty': 1.000, 'UnitPric': format(float(product['price']/100), '.2f'), 'PdctAmt': format(float(product['price']/100), '.2f')})
    return products_in_catalog

# def check_product(tsp_id):
    # не используется
    # prod = None
    # post_data = {"merchantIds": [tsp_id]}
    # prod = management_api.get_productNode(management_token, json.dumps(post_data))
    # assert prod.status_code == 200
    # prod = json.loads(prod.text.encode('utf-8').decode('utf-8-sig'))
    # for product in prod['data']:
    #     if product in prod['data']:
    #         product_id = product['id']
    #         break

def check_cards_wallet_NKO(cards, social_programm, tsp, check_cards_wallets_nko=True):
    # Работа с массивом карт, если check_cards_wallets_nko стоит true произовдиться проверка баланса в НКО
    hash_cards = []
    for card in cards:
        pan = sha1(bytes((str(card)), 'utf8')).hexdigest().upper() # получение хеша карты
        if check_cards_wallets_nko == True: # процедура проверки кошелька и баланса карты
            loger.info('Проверка карты {0} по счету {1} из {2}'.format(card, cards.index(card)+1, len(cards)))
            message = 'Всего счетов в НКО было или создано и пополнено'
            surrogate_name = pan+social_programm
            check_wallet = {"surrogate_name": surrogate_name, "project_id": tsp, "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce", "region_id": "39"}
            check_wallet = nko_api.get_wallet(json.dumps(check_wallet))
            assert check_wallet.status_code == 200, check_wallet.text
            check_wallet = json.loads(check_wallet.text.encode('utf-8').decode('utf-8-sig'))
            if check_wallet['code'] == 1050:
                loger.info('Кошелек для карты {0} не найден, создаём...'.format(card))
                add_wallet = {"surrogate_name": surrogate_name,  "name_ending": str(card), "region_id": "39", "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce"}
                add_wallet = nko_api.add_wallet(json.dumps(add_wallet))
                if add_wallet.status_code == 200:
                    add_wallet = json.loads(add_wallet.text.encode('utf-8').decode('utf-8-sig'))
                    if add_wallet['code'] == 1000:
                        loger.info('Кошелек для карты {0} успешно создан.'.format(card))
            trid = randint(1000000000000000,9999999999999999)
            time = (datetime.datetime.now()-datetime.timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S.%f+03:00")
            check_credit = {"id": trid, "amount": 999999, "surrogate_name": surrogate_name, "region_id": "39", "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce", "organisation_id": tsp, "time": time}
            check_credit = nko_api.check_credit(json.dumps(check_credit))
            if check_credit.status_code == 200:
                check_credit = json.loads(check_credit.text.encode('utf-8').decode('utf-8-sig'))
                max_ammount = check_credit['max_amount']
                loger.info('Кошелек карты {0} есть, макс сумма пополнения {1}'.format(card, max_ammount))
                if max_ammount > 0:
                    trid = randint(1000000000000000,9999999999999999)
                    add_credit = {"id": trid, "amount": max_ammount, "surrogate_name": surrogate_name, "region_id": "39", "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce", "organisation_id": tsp, "time": time}
                    add_credit = nko_api.add_credit(json.dumps(add_credit))
                    if add_credit.status_code == 200 and json.loads(add_credit.text.encode('utf-8').decode('utf-8-sig'))['code'] == 1000:
                        loger.info('Кошелек карты {0} пополнен на сумму {1}'.format(card, max_ammount))
                        hash_cards.append(pan)
                elif max_ammount == 0:
                    loger.info('Кошелек карты {0} имеет максимальный баланс {1}'.format(card, check_credit['balance']))
                    hash_cards.append(pan)
        elif check_cards_wallets_nko == False:
            hash_cards.append(pan)
            message = 'Всего карт без проверки в НКО'
    loger.info('{1} {0}'.format(len(hash_cards), message))
    return hash_cards

def cash_update():
    management_api.cache_update()