from datetime import datetime
import requests
import os

SHEETY_ENDPOINT = os.environ['SHEETY_ENDPOINT']
SHEETY_DELETE = os.environ['SHEETY_DELETE']
SHEETY_GAIN_LOSS = os.environ['SHEETY_GAIN_LOSS']
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")


def add_new_order(order_id, price, amount, order_type):
    price = float(price)
    amount = float(amount)
    sheet_inputs = {
        "datum": {
            "date": today_date,
            "time": now_time,
            "key": order_id,
            "price": price,
            "amount": amount,
            "order": order_type
        }
    }
    sheet_response = requests.post(SHEETY_ENDPOINT, json=sheet_inputs)
    print(sheet_response.text)


def get_gain_loss(avg_buy, price_sold, balance):
    pct_gain_loss = ((price_sold - avg_buy) / avg_buy) * 100
    sheet_inputs = {
        "datum": {
            "date": today_date,
            "time": now_time,
            "bought": avg_buy,
            "sold": price_sold,
            'balance': balance,
            "pct": pct_gain_loss,
        }
    }
    sheet_response = requests.post(SHEETY_GAIN_LOSS, json=sheet_inputs)
    print(sheet_response.text)


def update_order_data():
    response = requests.get(SHEETY_ENDPOINT)
    data_json = response.json()
    for _ in data_json['data']:
        requests.delete(SHEETY_DELETE + "2")
