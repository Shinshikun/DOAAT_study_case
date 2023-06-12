import requests
import urllib
import json
import config


class ActualGeneration():
    

    def __init__(self):
        self.access_token, self.token_type = self.get_token()

    def get_per_unit(self, start_date=None, end_date=None) -> dict:
        response = requests.get('https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_unit',
                                headers={'Authorization': f'{self.access_token} {self.token_type} '}
                               )

        if response.status_code == 200: #and 'application/json' in response.headers.get('Content-Type',''):
            return response.json()
        else:
            return response.status_code
    
    

    def get_token(self):

        response = requests.post('https://digital.iservices.rte-france.com/token/oauth/', 
                                 headers={"content-type": f"application/x-www-form-urlencoded", 
                                          "Authorization": f"Basic {config.SECRET_KEY}"}, 
                                )
        if response.ok:
            access_token = response.json()['access_token']
            token_type = response.json()['token_type']
        else:
            Warning("Impossible de se connecter")
            access_token = None
            token_type = None

        return token_type, access_token