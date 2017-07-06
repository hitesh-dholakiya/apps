
import requests
import base64
import hashlib
import hmac
import time


class OauthGen:

    def __init__(self):
        self.environment = {
            'client_id': 'dEGPKfHdRbYvGtzOZiq4LKSEdIPeJOyD',
            'client_secret': 'wCrViGZioG4NFEZp',
            'callback': 'www.autodesk.com',
            'oauth_authorization': None,
            'oauth_timestamp': None,
            'oauth_signature': None,
        }

    def get_token(self):
        client_id = self.environment['client_id']
        client_secret = self.environment['client_secret']
        callback = self.environment['callback']

        timestamp = int(round(time.time()))

        cred_str = client_id + ":" + client_secret
        base64_header = base64.b64encode(cred_str)

        base_str = callback + client_id + str(timestamp)
        hmacsha256 = hmac.new(client_secret, msg=base_str, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(hmacsha256).decode()

        self.environment['oauth_authorization'] = base64_header
        self.environment['oauth_timestamp'] = str(timestamp)
        self.environment['oauth_signature'] = signature

        oauthurl = "https://enterprise-api-dev.autodesk.com/v2/oauth/generateaccesstoken?grant_type=client_credentials"

        headers = {'Authorization':  'Basic ' + self.environment['oauth_authorization'],
                   'signature': self.environment['oauth_signature'], 'timestamp': self.environment['oauth_timestamp']}

        response = requests.post(oauthurl, headers=headers)
        return response.json()
#########
