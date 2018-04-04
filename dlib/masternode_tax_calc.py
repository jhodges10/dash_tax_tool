import datetime
from dlib.crypto_compare import CryptoCompare
from dlib import wallet_insights as wi


def get_cb_trans(address):
    cb_tx = wi.build_simple_wallet_history(address)
    #print(cb_tx)
    return cb_tx


def convert_timestamp_to_day(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')


def process_cb_trans(cb_trans):
    for tx in cb_trans:
        date = convert_timestamp_to_day(tx['time'])
        cost_usd = round((tx['amount'] * CryptoCompare.match_day_to_price(date)), 2)
        tx.update({'cost_basis': cost_usd})
        tx.update({'date': date})

    return cb_trans


def convert_list_to_dict(cb_trans):
    cb_dict = {}
    for tx in cb_trans:
        cb_dict[tx['date']] = {'amount': tx['amount'],
                               'type': tx['type'],
                               'cost_basis': tx['cost_basis']}

    return cb_dict


def generate_cost_basis(address='XxVpWcsE92qWTrZWfmGTqrCzpBaKhRf2tX'):
    trans = get_cb_trans(address)
    cost_basis = process_cb_trans(trans)

    return cost_basis

#mn_address = 'XxVpWcsE92qWTrZWfmGTqrCzpBaKhRf2tX'
#mn_address = 'XnhM7gomoHnYC54LipsXKoancngQDNsdwi'
#mn_address = 'XpKcgRUXZuM7M7JadAo5o7Q2XKes8nQfd5'

#print(generate_cost_basis())