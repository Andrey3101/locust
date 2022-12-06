
import requests
import logging

class NKOApi():
    def __init__(self, url):
        self.nko_url = url
        self.log = logging.getLogger("nko_api")

    def add_wallet(self, post_data):
        add_wallet_url = self.nko_url+'/cards/api/v1/surrogate/add'
        req = requests.post(add_wallet_url, headers = {"Content-Type": "application/json"}, data=post_data, verify=False)
        return req
    
    def get_wallet(self, post_data):
        get_wallet_url = self.nko_url+ '/cards/api/v1/wallet/get_data'
        req = requests.post(get_wallet_url, headers = {"Content-Type": "application/json"}, data=post_data, verify=False)
        return req
    
    def check_credit(self, post_data):
        check_wallet_url = self.nko_url+ '/transactions/api/v1/credit/check'
        req = requests.post(check_wallet_url, headers = {"Content-Type": "application/json"}, data=post_data, verify=False)
        return req

    def add_credit(self, post_data):
        add_credit_url = self.nko_url+ '/transactions/api/v1/credit/add'
        req = requests.post(add_credit_url, headers = {"Content-Type": "application/json"}, data=post_data, verify=False)
        return req