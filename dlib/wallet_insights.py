import requests
import json
from json import JSONDecodeError
import random
from multiprocessing import Pool
from functools import partial
from dlib import masternode_tax_calc as mtx

# Insight API
def fetch_wallet(address):
    url_1 = "https://insight.dashevo.org/insight-api-dash/addr/{}".format(address)
    url_2 = "https://insight.dash.org/insight-api-dash/addr/{}".format(address)
    url_3 = "http://insight.masternode.io:3000/api/addr/{}".format(address)
    url_4 = "http://165.227.209.32:3001/insight-api-dash/addr{}".format(address)
    urls = [url_1, url_2, url_3]

    url_selected = random.choice(urls)

    response = requests.request("GET", url_selected)
    try:
        transaction_list = json.loads(response.text)['transactions']
        # print(transaction_list)
        return transaction_list

    except KeyError:
        return []


# Insight API
def fetch_transaction_history(txid, address):

    url_1 = "https://insight.dashevo.org/insight-api-dash/tx/{}".format(txid)
    url_2 = "https://insight.dash.org/insight-api-dash/tx/{}".format(txid)
    url_3 = "http://insight.masternode.io:3000/api/tx/{}".format(txid)
    url_4 = "http://165.227.209.32:3001/insight-api-dash/tx/{}".format(txid)
    urls = [url_1, url_2, url_3]

    url_selected = random.choice(urls)

    response = requests.request("GET", url_selected)
    matching_transactions = False

    try:
        transaction_info = json.loads(response.text)

        if 'coinbase' in transaction_info['vin'][0].keys():
            for vout in transaction_info['vout']:
                # print(vout.keys())
                amount_to_address = float(vout['value'])
                if int(round(amount_to_address)) >= 5:
                    trans_type = 'superblock_payment'
                elif int(round(amount_to_address)) >= 1:
                    trans_type = 'mn_payment'
                else:
                    trans_type = 'mining_payment'
                try:
                    if address in vout['scriptPubKey']['addresses']:
                        trans_dict = {
                            "amount": amount_to_address,
                            "time": transaction_info['time'],
                            "type": trans_type
                        }
                        matching_transactions = trans_dict
                        print(matching_transactions)
                    else:
                        pass
                except KeyError or UnboundLocalError:
                    continue
        else:
            for vout in transaction_info['vout']:
                amount_to_address = float(vout['value'])
                trans_type = 'normal'
                try:
                    if address in vout['scriptPubKey']['addresses']:
                        trans_dict = {
                            "amount": amount_to_address,
                            "time": transaction_info['time'],
                            "type": trans_type
                        }
                        matching_transactions = trans_dict
                        print(matching_transactions)
                    else:
                        pass
                except KeyError or UnboundLocalError:
                    continue

        return matching_transactions

    except JSONDecodeError:
        print("Error with that transaction")
        null_dict = {
            "amount": 'Null',
            "time": 'Null',
            "date": 'Null',
            "type": 'Null'
        }
        return null_dict


# Insight API
def build_simple_wallet_history(address):
    transaction_list = fetch_wallet(address)
    num_of_processes = 12
    p = Pool(num_of_processes)
    matching_tx = p.map(partial(fetch_transaction_history, address=address), transaction_list)
    p.close()
    p.join()

    cleaned_transactions = []
    '''
    for count, txid in enumerate(transaction_list):
        count += 1
        print("Checking txid: " + str(txid))
        transaction_info = fetch_transaction_history(txid, address)
        if transaction_info is not False:
            cleaned_transactions.append(transaction_info)
        else:
            continue
    '''
    for tx_info in matching_tx:
        if tx_info is not False:
            cleaned_transactions.append(tx_info)
        else:
            continue

    return cleaned_transactions


# Chainz API
def pooled_address_history_request(list_of_addresses):
    url = "https://chainz.cryptoid.info/dash/api.dws"
    querystring = {"q": "multiaddr", "active": "{}".format(list_of_addresses), "n": "1000", "key": "deb339469dc2"}

    response = requests.request("GET", url, params=querystring)

    try:
        t_history = json.loads(response.text)
        return t_history
    except JSONDecodeError:
        return []


# Chainz API
def single_address_history_request(address):
    url = "https://chainz.cryptoid.info/dash/api.dws"
    querystring = {"q": "multiaddr", "active": "{}".format(address), "n": "1000", "key": "deb339469dc2"}

    response = requests.request("GET", url, params=querystring)

    try:
        t_history = json.loads(response.text)

        for transaction in t_history['txs']:
            #print(transaction)
            transaction['change'] = transaction['change']/100000000

        return t_history
    except JSONDecodeError as e:
        return e

