
import requests
import json
import logging
import urllib3

urllib3.disable_warnings()

class ManagementApi():
    def __init__(self, url):
        self.m_url = url
        self.log = logging.getLogger("management_api")

    def get_oiv(self, management_token, post_data):
        m_auth_url = self.m_url+'/executiveauthority/search'
        
        req = requests.post(m_auth_url, headers = {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data=post_data, verify=False)
        return req
    
    def create_oiv(self, management_token, post_data):
        m_auth_url = self.m_url+'/executiveauthority'
        req = requests.post(m_auth_url, headers = {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data=post_data, verify=False)
        return req

    def creat_social_program(self,management_token, post_data):
        # Социальная программа
        creat_social_program_url = self.m_url + '/socialprogram'
        self.log.debug(creat_social_program_url)
        req = requests.post(creat_social_program_url, headers = {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data=post_data, verify=False)
        return req

    def get_social_programs(self, management_token, post_data):
        get_s_program_url = self.m_url + '/socialprogram/search'
        req = requests.post(get_s_program_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data=post_data, verify=False)
        return req

    def get_social_program_by_id(self, management_token, id):
        get_s_program_url = self.m_url + '/socialprogram/'+str(id)
        req = requests.get(get_s_program_url, headers= {"Authorization": "Bearer " + management_token}, verify=False)
        return req

    def get_benefittype(self, management_token, post_data):
        get_s_program_url = self.m_url + '/benefittype/search'
        req = requests.post(get_s_program_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data=post_data, verify=False)
        return req
        

    def add_benefittype(self, management_token, post_data):
        # Социальная программа
        add_social_program_url = self.m_url + '/benefittype'
        self.log.debug(add_social_program_url)
        req = requests.post(add_social_program_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data=post_data, verify=False)
        return req

    def create_tsp(self, management_token, post_data):
        #ТСП
        create_tsp_url = self.m_url + '/merchant'
        self.log.debug(create_tsp_url)
        req = requests.post(create_tsp_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def get_tsp(self, management_token, post_data):
        # ТСП
        get_tsp_url = self.m_url + '/merchant/search'
        self.log.debug(get_tsp_url)
        req = requests.post(get_tsp_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def create_shop(self, management_token, post_data):
        # Создание магазина
        creare_shop_url = self.m_url + '/shop'
        self.log.debug(creare_shop_url)
        req = requests.post(creare_shop_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def get_shopNode(self, management_token, post_data):
        # Магаз
        get_shop_url = self.m_url + '/shop/search'
        self.log.debug(get_shop_url)
        req = requests.post(get_shop_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def create_terminal(self, management_token, post_data):
        # Создание терминала
        create_terminal_url = self.m_url + '/terminal'
        self.log.debug(create_terminal_url)
        req = requests.post(create_terminal_url, headers= {"Content-Type": "apllication/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def get_terminalNode(self, management_token, post_data):
        # Терминал
        get_terminal_url = self.m_url + '/terminal/search'
        self.log.debug(get_terminal_url)
        req = requests.post(get_terminal_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def get_productNode(self, management_token, post_data):
        # Проверка продукта
        get_product_url = self.m_url + '/product/search'
        self.log.debug(get_product_url)
        req = requests.post(get_product_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def create_product(self, management_token, post_data):
        # Создание продукта
        create_product_url = self.m_url + '/productcatalog/product'
        self.log.debug(create_product_url)
        req = requests.post(create_product_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def create_catalog(self, management_token, post_data):
        # Создание каталога товаров
        create_catalog_url = self.m_url + '/productcatalog'
        self.log.debug(create_catalog_url)
        req = requests.post(create_catalog_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer "+ management_token}, data= post_data, verify=False)
        return req
    
    def get_catalogs(self, management_token, post_data):
        # Получение каталогов товаров
        get_catalogs_url = self.m_url + '/productcatalog/search'
        self.log.debug(get_catalogs_url)
        req = requests.post(get_catalogs_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer "+ management_token}, data= post_data, verify=False)
        return req

    def get_product_catalog_product(self, management_token, post_data):
        # Проверка товара в каталоге товаров
        get_product_product_url = self.m_url + '/productcatalog/product/search'
        self.log.debug(get_product_product_url)
        req = requests.post(get_product_product_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req
    
    def create_product_catagory(self, management_token, post_data):
        #Создание катагории товаров
        create_product_catagory_url = self.m_url + '/productcategory'
        self.log.debug(create_product_catagory_url)
        req = requests.post(create_product_catagory_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def get_product_category(self, management_token, post_data):
        # Получение всех категорий товаров
        get_product_category_url = self.m_url + '/productcategory/search'
        self.log.debug(get_product_category_url)
        req = requests.post(get_product_category_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def matching_catalog(self, management_token, put_data, full=False):
        if full == False:
            get_product_category_url = self.m_url + '/productcatalog/matching'
        else:
            get_product_category_url = self.m_url + '/productcatalog/fullyMatching'
        self.log.debug(get_product_category_url)
        req = requests.put(get_product_category_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= put_data, verify=False)
        return req

    def cache_update(self):
        # Принудительное обновление кэша
        get_cache_update_url = self.m_url + '/cacheupdate'
        self.log.debug(get_cache_update_url)
        req = requests.get(get_cache_update_url, verify=False)
        return req

    def authorize (self, login, password):
        # Авторизация
        auth = json.loads('{"login": "", "password": ""}')
        auth['login'] = login
        auth['password'] = password
        m_auth_url = self.m_url+'/auth/login'
        self.log.debug(m_auth_url)
        post_data = json.dumps(auth)
        self.log.debug(post_data, verify=False)
        req = requests.post(m_auth_url, headers = {"Content-Type": "application/json"}, data=post_data, verify=False)
        return req