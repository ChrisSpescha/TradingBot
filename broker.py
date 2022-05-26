import datamanager
import base64
import datetime
import hashlib
import hmac
import json
import time
import os
import requests

base_url = "https://api.sandbox.gemini.com"
endpoint = "/v1/order/new"
buy_url = base_url + endpoint

gemini_api_key = os.environ["GEMINI_API"]
gemini_api_secret = os.environ['API_SECRET'].encode()

t = datetime.datetime.now()
payload_nonce = str(int(time.mktime(t.timetuple()) * 1000))

# Get Current BTC Price from Gemini Exchange
btc_data = requests.get(base_url + "/v2/candles/btcusd/1hr")
btc_data_json = btc_data.json()
current_price = btc_data_json[0][4]
price_string = str(current_price)


def place_order(order_type, amount):

    payload = {
        "request": "/v1/order/new",
        "nonce": payload_nonce,
        "symbol": "btcusd",
        "amount": amount,
        "price": price_string,
        "side": order_type,
        "type": "exchange limit",
        "options": ["maker-or-cancel"]
    }

    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': b64,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache",
                       }

    response = requests.post(buy_url,
                             data=None,
                             headers=request_headers)
    new_order = response.json()

    if not new_order['is_cancelled']:
        datamanager.add_new_order(new_order['order_id'],
                                  new_order['price'],
                                  new_order['original_amount'],
                                  new_order['side'])
