import requests
import os
from dotenv import load_dotenv
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
api_key = 'a key'
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

def get_data():
    """Calls the api and returns the value from the key pair data. If there is 
        an error, it returns a string of the error message.

    Returns
    -------
    dict
        A dictionary containing the data of all the cryptocurrencies in the api
    str
        Returns a string if there is an error

    """
    response = requests.get(url, headers=headers)
    response_json = response.json()
    if response_json.get('data') == None:
        return response_json['status']['error_message']
    return response_json


def search_coin(coin_name):
    """Calls the function get_data and finds the cryptocurrency from the user-given
        coin_name. If the coin is not found, an error message is returned.

    Parameters
    ----------
    coin_name : str
        The user-given name of the coin they want

    Returns
    -------
    dict
        A dictionary containing the data the api has on the cryptocurrency
    str
        Returns a string with the message "Not found" if there is an error
    """
    data = get_data()
    for i in data["data"]:
        if coin_name.lower() == i["symbol"].lower() or coin_name.lower() == i["name"].lower():
            return i

    return "Not found"

def get_crypto_price(dic):
    """Calls the function get_data and finds the cryptocurrency from the user-given
        coin_name. If the coin is not found, an error message is returned.

    Parameters
    ----------
    coin_name : str
        The user-given name of the coin they want

    Returns
    -------
    dict
        A dictionary containing the data the api has on the cryptocurrency
    str
        Returns a string with the message "Not found" if there is an error
    """
    return float(dic["quote"]["USD"]["price"])
    

    
