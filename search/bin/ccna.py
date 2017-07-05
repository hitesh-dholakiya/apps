from auth import OauthGen
import base64
import time
import hashlib
import hmac
import requests
import json

my_tokengen = OauthGen()
token = my_tokengen.get_token()

client_id = my_tokengen.environment['client_id']
client_secret = my_tokengen.environment['client_secret']
callback = my_tokengen.environment['callback']

timestamp = int(round(time.time()))

cred_str = client_id + ":" + client_secret
base64_header = base64.b64encode(cred_str)

session_id = token['access_token']
base_str = callback + session_id + str(timestamp)
hmacsha256 = hmac.new(client_secret, msg=base_str, digestmod=hashlib.sha256).digest()
api_signature = base64.b64encode(hmacsha256).decode()

ccnaurl = 'https://enterprise-api-stg.autodesk.com/eis-abus/v1/ccna'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + session_id, 'CSN': '5122424540',
           'signature': api_signature,
           'timestamp': str(timestamp)}

payload = {
 "caseOrigin":"AKN",
 "caseSubOrigin":"Otto",
 "serviceContractNo": "110001948762",
 "description":"Chat history",
 "accountName": "",
 "addressLine1": "1 McInnis Pkwy",
 "addressLine2": "",
 "addressLine3": "",
 "city": "San Rafael",
 "state": "CA",
 "postalCode": "94903-2764",
 "country": "United States",
 "currentCMEmail":"shardul.khodankar@autodesk.com",
 "reqFirstName":"Juhi",
 "reqLastName":"Barai",
 "reqEmail":"shardul.khodankar@autodesk.com",
 "reqCountry":"US",
 "reqLanguage":"EN"
}

response = requests.post(ccnaurl, data=json.dumps(payload), headers=headers)

print json.dumps(response.json())
