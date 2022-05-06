import datamanager
import requests
import broker
import time
import os

order_avg = 0
indicator = "rsi"
rsi_endpoint = f"https://api.taapi.io/{indicator}"
base_url = "https://api.sandbox.gemini.com/v2"
sheety_get = os.environ['SHEETY_ENDPOINT']
btc_data_endpoint = requests.get(base_url + "/candles/btcusd/1hr")

btc_data_json = btc_data_endpoint.json()
current_price = btc_data_json[0][4]

response = requests.get(sheety_get)
data_json = response.json()

order_list = []
for order in data_json['data']:
    order_list.append(order['price'])

if order_list:
    order_avg = round(sum(order_list) / len(order_list), 2)

balance = 0
for order in data_json['data']:
    balance += order['amount']


params = {
    "secret": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IkNzcGVzaEBsaXZlLmNvbSIsImlhdCI6MTY1MTc0ODQ4NywiZXhwIjo"
              "3OTU4OTQ4NDg3fQ.39jl63Bzsc0QKTvcRf3bfeyrMDuc2JvaPFOw3g_vF_0",
    "exchange": "binance",
    "symbol": "BTC/USDT",
    "interval": "1h"
}
# Retrieve Rsi Data
rsi_response = requests.get(url=rsi_endpoint, params=params)
rsi_json = rsi_response.json()
rsi = rsi_json['value']

count = 0
trade = True
while count < 5 and trade:
    if rsi < 30:
        broker.place_order('buy', '.001')
        trade = False
    elif order_avg != 0:
        if rsi > 50 and current_price > order_avg:
            broker.place_order('sell', f"{balance}")
            datamanager.get_gain_loss(order_avg, current_price, balance)
            datamanager.update_order_data()
            trade = False
        elif order_avg < current_price:
            pct_gain_loss = ((current_price - order_avg) / order_avg) * 100
            if pct_gain_loss < -3:
                broker.place_order('sell', f"{balance}")
                datamanager.get_gain_loss(order_avg, current_price, balance)
                datamanager.update_order_data()
                trade = False
    else:
        count += 1
        time.sleep(1)
