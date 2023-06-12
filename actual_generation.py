import requests
import datetime
import urllib
import pandas as pd
import dateutil.parser 
from typing import Optional

import config



class ActualGeneration():
    

    def __init__(self):
        self.access_token, self.token_type = self.get_token()

    def get_per_unit(self, start_date: Optional[datetime.datetime] = None, end_date: Optional[datetime.datetime] = None, sandbox=True) -> dict:

        if sandbox:
            url = "https://digital.iservices.rte-france.com/open_api/actual_generation/v1/sandbox/actual_generations_per_unit"
        else:
            url = "https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_unit"


        if start_date is None or end_date is None:
            response = requests.get(url,
                                    headers={'Authorization': f'{self.access_token} {self.token_type} '})
        else:
            start = start_date.strftime("%Y-%m-%dT%H:%M:%S+02:00")
            end = end_date.strftime("%Y-%m-%dT%H:%M:%S+02:00")
            param = urllib.parse.urlencode({"start_date": start, "end_date": end}).replace("%3A", ":")
            response = requests.get(url,
                                    headers={'Authorization': f'{self.access_token} {self.token_type} '},
                                    params=param
                                )

        if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type',''):
            return response.json()
        else:
            return response.status_code

    
    def get_mean_hour_by_hour(self, start_date: Optional[datetime.datetime] = None, end_date: Optional[datetime.datetime] = None, sandbox=True):
        data = self.get_per_unit(start_date, end_date, sandbox=sandbox)
        value_per_hour = {}
        if type(data) != dict:
            print("Erreur lors de l'appel à l'API")
            return
        data = data.get("actual_generations_per_unit")

        for entry in data:
            for values in entry["values"]:
                date = dateutil.parser.parse(values["start_date"])
                if date in value_per_hour:
                    value_per_hour[date] += values["value"]
                else:
                    value_per_hour[date] = values["value"]

        d = pd.Series(value_per_hour).resample("H").mean()
        print(d)


    def get_token(self):

        response = requests.post(config.URL_AUTH, 
                                 headers={"content-type": f"application/x-www-form-urlencoded", 
                                          "Authorization": f"Basic {config.SECRET_KEY}"}
                                )
        if response.ok:
            access_token = response.json()['access_token']
            token_type = response.json()['token_type']
        else:
            Warning("Impossible de se connecter")
            access_token = None
            token_type = None

        return token_type, access_token