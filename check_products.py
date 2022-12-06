import logging
import json
import random
import locust_setup
from  gen_credit_card_number import credit_card_number

logging.basicConfig(level=logging.INFO)
loger = logging.getLogger("Check Wallets NKO")

# Получение основных конфигурационных данных из settings.json
configfile = open('settings.json', 'r')
settings = json.loads(configfile.read())
region = settings['region_id']
seed = settings['seed']
count_cards = settings['count_gen_cards']
loger.info('Кол-во генерируемых карт: {0}, проверка в НКО кошельков у карт {1}'.format(count_cards, True))
count_product_in_catalog = settings['count_product_in_catalog']

random.seed(seed) # параметр влияет на генерацию карт, благодаря которому массив например 100 карт будет всегда одиннаковый
cards = credit_card_number(16, count_cards)
random.seed()
oiv_id = locust_setup.check_oiv(region) # проверка соц.учреждения
benefitTypeId = locust_setup.check_benefittype(region) #проверка категории льгот
social_program_id, social_program_code = locust_setup.check_social_program(region, benefitTypeId, oiv_id) #проверка соц.программы
tsp_id, tsp_code = locust_setup.check_TSP(region, social_program_id) #Проверка ТСП (Торг.предприятия)
product_category = locust_setup.check_product_category(tsp_id) #Проверка наличия продуктовой категории(й)
products = locust_setup.check_catalog(tsp_id, social_program_id, count_product_in_catalog, product_category, oiv_id)