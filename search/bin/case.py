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

caseurl = 'https://enterprise-api-stg.autodesk.com/eis-abus/v1/case'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + session_id, 'CSN': '5122424540',
           'signature': api_signature,
           'timestamp': str(timestamp)}

payload = {
  "origin":"AKN",
  "subOrigin":"Otto",
  "Description" : "chat history",
  "subject" : "Change Company Name or Address",
  "Email":"Juhi.barai@autodesk.com",
  "RequestorEmail":"shardul.khodankar@autodesk.com",
  "caseType" : "CCNA",
  "newAddress" : "111 McInnis Pkwy, San Rafael, CA, 94903, US",
  "reqFname" : "S",
  "reqLname" : "K",
  "subscriptionNumber" : "110000869990",
  "accountId" : "001n000000DrOc5AAF",
  "companyName" : "New Company Name",
  "previousCompanyName" : "Old Company Name",
  "addressLine1" : "Old address line 1",
  "addressLine2" : "Old address line 2",
  "addressLine3" : "Old address line 3",
  "city" : "old city",
  "systemName": "VA"
}

response = requests.post(caseurl, data=json.dumps(payload), headers=headers)

#print json.dumps(response.json())
for i in response.json():
    print json.dumps(i)
