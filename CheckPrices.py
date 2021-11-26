import requests
import os
from dotenv import load_dotenv
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
api_key = '00e106e1-ada5-444d-878e-6f7f079c11a5'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
}


'''
response_json is a dictionary that looks like:
    {
        "data" : [list of dictionaries of each coin]
        "status" : {status}
    }
'''
#Gets the data dict from the dict
def get_data():
    response = requests.get(url, headers=headers)
    response_json = response.json()
    if response_json.get('data') == None: #if data isn't found, there was an error
        return response_json['status']['error_message']
    return response_json

#returns a dictionary with the coin info
def search_coin(coin_name):
    data = get_data()
    for i in data["data"]:
        if coin_name.lower() == i["symbol"].lower() or coin_name.lower() == i["name"].lower():
            return i
    return "Not found"

def get_crypto_price(dic):
    return float(dic["quote"]["USD"]["price"])
    

    
