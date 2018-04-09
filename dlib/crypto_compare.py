import requests
import json
import os
import time
import functools


class CryptoCompare:
    def _init_(self):
        pass

    @staticmethod
    @functools.lru_cache(maxsize=24)
    def fetch_price_history_dict(use_cache=False, days_to_fetch=1500):
        storage_location = "./_cache/price_history.json"

        # TODO add age of cache as conditional element
        #file_age = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(storage_location)))

        if use_cache and os.path.isfile(storage_location):
                day_and_price_dict = CryptoCompare.read_json("price_history")
        else:
            url = "https://min-api.cryptocompare.com/data/histoday"
            querystring = {"fsym": "DASH", "tsym": "USD", "limit": "{}".format(days_to_fetch), "e": "CCCAGG"}
            response = requests.request("GET", url, params=querystring)
            historical_data = json.loads(response.text)

            day_and_price_dict = {}

            for day in historical_data['Data']:
                date = time.strftime('%Y-%m-%d', time.localtime(day.pop('time')))
                price = day['close']
                day_and_price_dict[date] = price

            try:
                CryptoCompare.write_json(day_and_price_dict, "price_history")
            except:
                print("Running on Heroku, memoizing instead.")

        return day_and_price_dict

    @staticmethod
    def fetch_cur_price():
        url = 'https://min-api.cryptocompare.com/data/price?fsym=DASH&tsyms=USD'
        response = requests.request("GET", url)

        if response.status_code == 200:
            price = json.loads(response.text)['USD']
            print(price)
            return price
        else:
            return None

    @staticmethod
    def match_day_to_price(date):
        try:
            day_and_price = CryptoCompare.fetch_price_history_dict(use_cache=False)
            price = day_and_price[date]
        except KeyError as e:
            print("Error: " + str(e))
            try:
                # If we fail the first time, we go back and try it without the cache
                day_and_price = CryptoCompare.fetch_price_history_dict(use_cache=False)
                price = day_and_price[date]
            except KeyError as e:
                # Fetch current price because it's from today, that's why we couldn't get historical data
                price = CryptoCompare.fetch_cur_price()
                print("Error: " + str(e))

        return price

    @staticmethod
    def write_json(data, filename):
        cache_dir = './_cache/'
        dirname = os.path.dirname(os.path.abspath(__file__))
        absolute_cache_dir = os.path.abspath(os.path.join(dirname, cache_dir))
        filename = filename + '.json'
        absolute_file_path = os.path.abspath(os.path.join(absolute_cache_dir, filename))

        with open(absolute_file_path, 'w') as json_stuff:
            json.dump(data, json_stuff)
        return True

    @staticmethod
    def read_json(filename):
        cache_dir = './_cache/'
        dirname = os.path.dirname(os.path.abspath(__file__))
        absolute_cache_dir = os.path.abspath(os.path.join(dirname, cache_dir))
        filename = filename + '.json'
        absolute_file_path = os.path.abspath(os.path.join(absolute_cache_dir, filename))

        try:
            with open(absolute_file_path, 'r') as json_stuff:
                data_dict = json.loads(json_stuff)
        except TypeError as e:
            try:
                with open(absolute_file_path, 'r') as json_stuff:
                    json_stuff = json_stuff.read()
                    data_dict = json.loads(json_stuff)
            except Exception as e:
                print(e)
                data_dict = {}
        return data_dict