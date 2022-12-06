from locust import HttpUser, TaskSet, task, between, events

import logging
import json
import random
import locust_setup
from  gen_credit_card_number import credit_card_number
from gen_xml_transaction import xml_gen
from datetime import datetime
from uuid import uuid4
import urllib3

urllib3.disable_warnings()

gen = xml_gen()

loger = logging.getLogger("locust")
loger.setLevel(logging.INFO)

# Получение основных конфигурационных данных из settings.json
configfile = open('settings.json', 'r')
settings = json.loads(configfile.read())
region = settings['region_id']
wait_time = settings['wait_time']
seed = settings['seed']
TS_url = settings['terminal_system']
AcceptorAuthorisation = settings['weight_attribute']['AcceptorAuthorisation']
AcceptorBatchTransfer = settings['weight_attribute']['AcceptorBatchTransfer']

count_product_in_catalog = settings['count_product_in_catalog']
count_products_in_batch = settings['count_products_in_batch']
count_cards = settings['count_gen_cards']
check_cards_wallets_nko = settings['check_cards_wallets_nko']

@events.test_start.add_listener
def on_test_start(**kwargs):
# Исполняется проверка тестовых данных при каждом запуске НТ
    loger.info('Время между запросами между запросами для каждого потока составляет от {0} до {1}'.format(wait_time[0],wait_time[1]))
    loger.info('Кол-во генерируемых карт: {0}, проверка в НКО кошельков у карт {1}'.format(count_cards, check_cards_wallets_nko))
    random.seed(seed) # параметр влияет на генерацию карт, благодаря которому массив например 100 карт будет всегда одиннаковый
    cards = credit_card_number(16, count_cards)
    random.seed()
    # стартует перед генерацией user'ов, тут можно сделать проверку магазинов, терминалов и т.п.
    terminal_count = (kwargs['environment'].runner.target_user_count) # получение кол-во потоков/users
    loger.info('Кол-во генерируемых касс {0}'.format(terminal_count))
    oiv_id = locust_setup.check_oiv(region) # проверка соц.учреждения
    benefitTypeId = locust_setup.check_benefittype(region) #проверка категории льгот
    social_program_id, TaskSet.social_program_code = locust_setup.check_social_program(region, benefitTypeId, oiv_id) #проверка соц.программы
    tsp_id, TaskSet.tsp_code = locust_setup.check_TSP(region, social_program_id) #Проверка ТСП (Торг.предприятия)
    shop_id, TaskSet.shop_code = locust_setup.check_shop(tsp_id) #Проверка магазина
    TaskSet.terminals = locust_setup.check_terminal(shop_id, tsp_id, terminal_count) #Проверка касс (терминалов)
    product_category = locust_setup.check_product_category(tsp_id) #Проверка наличия продуктовой категории(й)
    TaskSet.products = locust_setup.check_catalog(tsp_id, social_program_id, count_product_in_catalog, product_category, oiv_id) # проверка каталога и товаров в каталоге, также проверка кол-во товаров в каталоге
    TaskSet.hash_cards = locust_setup.check_cards_wallet_NKO(cards, TaskSet.social_program_code, TaskSet.tsp_code, check_cards_wallets_nko) # проверка и получение хешей сгенерированных карт
    locust_setup.cash_update()


@events.test_stop.add_listener
def on_test_stop(**kwargs):
    # стартует после остановки теста нагрузки (остановка теста)
    loger.info('Делаем что-то после завершения теста')


class MyTaskSet(TaskSet):

    def on_start(self):
        # стартует для каждого user'a (user это один поток)
        try:
            self.terminal = TaskSet.terminals.pop() #присвоение номера кассы (терминалы)
        except AttributeError:
            self.user.environment.runner.quit()
        # self.succes_auth_req = [] не используется в текущей версии
        loger.info('Кассе присвоен номер {0}!'.format(self.terminal))

    @task(AcceptorAuthorisation)
    def AcceptorAuthorisationRequest(self):
        # генерация и отправка резерва
        time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00'
        CardData = random.choice(TaskSet.hash_cards)
        idref = str(uuid4())
        # idref = 'A_'+str(random.randint(0,9999))+'.'+ ''.join(random.choice('1234567890') for i in range(8)) + '.'+str(random.randint(0,9999)) + str(random.randint(0,9999))
        TxDtls = {'Ccy':TaskSet.social_program_code, 'TtlAmt':0.00}
        TxDtls['Pdct'] = []
        for x in range(random.randint(count_products_in_batch[0],count_products_in_batch[1])):
            TxDtls['Pdct'].append(TaskSet.products[x-1])
        TtlAmtArray = []
        for Amt in TxDtls['Pdct']:
            TtlAmtArray.append(float(Amt['PdctAmt']))
        TxDtls['TtlAmt'] = sum(TtlAmtArray)
        del(TtlAmtArray)
        AcceptorAuthorisationRequest = gen.AcceptorAuthorisationRequest(time, TaskSet.tsp_code, TaskSet.shop_code, self.terminal, '0000000000000000', '2023-09', CardData, time, idref, TxDtls).decode('UTF-8')
        AcceptorAuthorisationResponse = self.client.post(TS_url+'/acceptor/acceptorAuthorization',headers={"Content-type":"applicatqqion/json"},data=AcceptorAuthorisationRequest, name="Резервирование товаров", verify=False)
        # генерация запроса списание средств на основании полученого ответа резерва
        auth_code = gen.get_text_node(AcceptorAuthorisationResponse.text, 'urn:iso:std:iso:20022:tech:xsd:caaa.002.001.01', 'AuthstnCd')
        succes_auth_req = {'CardData': CardData, "TtlAmt": TxDtls['TtlAmt'], "auth_code": auth_code, "idref": idref, "TxDtTm": time}
        # transactoin_batch_id = 'B_'+str(random.randint(0,9999))+'.'+ ''.join(random.choice('1234567890') for i in range(8)) + '.'+str(random.randint(0,9999)) + str(random.randint(0,9999))
        transactoin_batch_id = str(uuid4())
        batch_time = (datetime.now())
        AcceptorBatchTransferRequest = gen.AcceptorBatchTransferRequest(batch_time, TaskSet.tsp_code, TaskSet.shop_code, self.terminal, '0000000000000000', '2023-09', succes_auth_req['CardData'], succes_auth_req['TxDtTm'], succes_auth_req['idref'], TxDtls, transactoin_batch_id, succes_auth_req['auth_code']).decode('UTF-8')
        AcceptorBatchTransferResponse = self.client.post(TS_url+'/acceptor/acceptorBatchTransfer',headers={"Content-type":"applicatqqion/json"},data=AcceptorBatchTransferRequest, name="Списание со счета", verify=False)
        pass

class MyLocust(HttpUser):
    tasks = {MyTaskSet:1}
    wait_time = between(wait_time[0], wait_time[1])
