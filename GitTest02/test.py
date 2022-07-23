import base64
import hashlib
import hmac
import time
import requests
import json
from filters import *




def send(phone):
    url = "https://sens.apigw.ntruss.com"
    uri = "/sms/v2/services/" + 'ncp:sms:kr:289640846112:sms_auth' + "/messages"
    api_url = url + uri
    timestamp = str(int(time.time() * 1000))
    access_key = '22lhKDJsMNwqsoCPyT0P'
    string_to_sign = "POST " + uri + "\n" + timestamp + "\n" + access_key
    signature = make_signature(string_to_sign)

    # 예약내역 불러와서 변환
    phone = phone.replace("-", "")
    name = '길동'
    booking_date = 1000

    message = "{}님 bernini 예약이 승인되었습니다.\n예약일자: {}".format(name, booking_date)

    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signature
    }

    body = {
        "type": "SMS",
        "contentType": "COMM",
        "from": "01030496533",
        "content": message,
        "messages": [{"to": phone}]
    }

    body = json.dumps(body)

    response = requests.post(api_url, headers=headers, data=body)
    response.raise_for_status()


def make_signature(string):
    secret_key = bytes('5rmLIdLmEawi2diWCXDAGgnVSOLIGzE7h9MoFj5y', 'UTF-8')
    string = bytes(string, 'UTF-8')
    string_hmac = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
    string_base64 = base64.b64encode(string_hmac).decode('UTF-8')
    return string_base64

send('01030496533')