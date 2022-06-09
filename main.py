import datamanager
import pandas as pd
import requests
import broker
import time
import os

balance = 0
order_avg = 0
indicator = "rsi"
rsi_endpoint = f"https://api.taapi.io/{indicator}"
base_url = "https://api.sandbox.gemini.com/v2"

# Current BTC Price via Gemini API
btc_data_endpoint = requests.get(base_url + "/candles/btcusd/1hr")
btc_data_json = btc_data_endpoint.json()
current_price = btc_data_json[0][4]

price_list = []  # list of order prices in balance.csv
orders_df = pd.read_csv('balance.csv')
for index, row in orders_df.iterrows():
    price_list.append(row['Price'])
# Avg buy price
if price_list:
    order_avg = round(sum(price_list) / len(price_list), 2)
# Current BTC balance
for index, row in orders_df.iterrows():
    balance += row['Amount']

params = {
    "secret": os.environ['TA_SECRET'],
    "exchange": "binance",
    "symbol": "BTC/USDT",
    "interval": "1h"
}
# Retrieve Rsi Data
# rsi_response = requests.get(url=rsi_endpoint, params=params)
# rsi_json = rsi_response.json()
# rsi = rsi_json['value']
rsi = 25

count = 0
trade = True
while count < 5 and trade:
    if rsi < 30:
        broker.place_order('buy', '.001')
        trade = False
    elif order_avg != 0:
        if rsi > 50 and balance > 0 and current_price > order_avg:
            rounded_balance = round(balance, 4)
            broker.place_order('sell', f"{rounded_balance}")
            datamanager.new_sell_order(order_avg, current_price, rounded_balance)
            datamanager.update_order_data()
            trade = False
        elif order_avg < current_price:
            pct_gain_loss = ((current_price - order_avg) / order_avg) * 100
            if pct_gain_loss < -3:
                broker.place_order('sell', f"{balance}")
                datamanager.new_sell_order(order_avg, current_price, balance)
                datamanager.update_order_data()
                trade = False
    else:
        count += 1
        time.sleep(1)
