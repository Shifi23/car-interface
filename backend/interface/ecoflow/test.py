import requests
import time
import hashlib
import hmac

ACCESS_KEY = "LPpAzKd0LYU084JWiHFDP5ZnrQTvNJKM"
SECRET_KEY = "wwsQPpNftPvTmCxGQrxoXsxRi7x7s22p"

def quota(serial_number):
    nonce = 537642
    timestamp = str(int(time.time() * 1000))
    # signed = "sn={}&accessKey={}&nonce={}&timestamp={}".format(serial_number, ACCESS_KEY, nonce, timestamp)
    signed = "accessKey={}&nonce={}&timestamp={}".format(ACCESS_KEY, nonce, timestamp)
    signature = sign(signed, SECRET_KEY)
    print(signature)

    # url = "https://api-e.ecoflow.com/iot-open/sign/device/quota/all?sn={}".format(serial_number)
    # url = "https://api-a.ecoflow.com/iot-open/sign/device/list"
    url = "https://api-a.ecoflow.com/iot-open/sign/certification"
    headers = {
        "accessKey": ACCESS_KEY,
        "timestamp": timestamp,
        "nonce": str(nonce),
        "sign": signature
    }

    response = requests.get(url, headers=headers)
    print(response.text)

def sign(data, key):
    signature_bytes = hmac.new(key.encode('utf-8'), msg=data.encode('utf-8'), digestmod=hashlib.sha256).digest()
    return signature_bytes.hex()


quota("R601ZAB7XFA71759")