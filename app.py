from flask import Flask, request, jsonify
import requests
import time
import hmac
import hashlib
import base64
import json

app = Flask(__name__)

API_KEY = "a2db7ec3-f32d-4a1e-948f-28694966d11b"
SECRET_KEY = "C4ABF417156E926544D93972C2ED266F"
PASSPHRASE = "BilalWaleed99@"
WITHDRAW_ADDRESS = "TB1YSAv2u6UMKS3v6z99sHVqgDRCpvtX1u"
CURRENCY = "USDT"
CHAIN = "USDT-TRC20"

def get_timestamp():
    return str(time.time())

def sign(message, secret_key):
    return base64.b64encode(hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()).decode()

def make_headers(method, path, body=""):
    timestamp = get_timestamp()
    message = timestamp + method + path + body
    signature = sign(message, SECRET_KEY)
    return {
        'OK-ACCESS-KEY': API_KEY,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': PASSPHRASE,
        'Content-Type': 'application/json'
    }

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json()
    amount = data.get("amount")
    
    if not amount or float(amount) <= 0:
        return jsonify({"message": "المبلغ غير صالح"}), 400

    body = {
        "ccy": CURRENCY,
        "amt": str(amount),
        "dest": "4",
        "toAddr": WITHDRAW_ADDRESS,
        "chain": CHAIN,
        "fee": "0.5"
    }

    path = "/api/v5/asset/withdrawal"
    url = "https://www.okx.com" + path
    headers = make_headers("POST", path, json.dumps(body))

    res = requests.post(url, headers=headers, json=body)

    if res.status_code == 200:
        return jsonify({"message": "تم إرسال السحب بنجاح"})
    else:
        print("خطأ بالسحب:", res.text)
        return jsonify({"message": "فشل في تنفيذ السحب"}), 500

if __name__ == '__main__':
    app.run(debug=True)
