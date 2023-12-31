import requests
import datetime
import urllib
import pandas as pd
from typing import Optional
import api.config as config


class ActualGeneration():
    """
    Class permettant de récupérer les informations
    de l'API RTE Actual Generation
    """

    def __init__(self):
        self.token_type, self.access_token = self.get_token()

    def get_per_unit(self,
                     start_date: Optional[datetime.datetime] = None,
                     end_date: Optional[datetime.datetime] = None,
                     sandbox=False):
        """
        Récupère les données de productions par unités.

        :param start_date: Date de départ des datas
        :param end_date: Date de fin des datas
        :param sandbox: S'il faut utiliser l'URL sandbox pour les tests
        """

        # La Sandbox permet de faire des tests avec moins de données
        if sandbox:
            url = ("https://digital.iservices.rte-france.com/open_api/"
                   "actual_generation/v1/sandbox/actual_generations_per_unit")
        else:
            url = ("https://digital.iservices.rte-france.com/open_api/"
                   "actual_generation/v1/actual_generations_per_unit")

        # Si la date de départ et de fin ne sont pas données, on get l'URL sans
        # paramètre
        if start_date is None or end_date is None:
            response = requests.get(
                url, headers={
                    'Authorization': f'{self.token_type} {self.access_token}'})
        else:
            start = start_date.strftime("%Y-%m-%dT%H:%M:%S+02:00")
            end = end_date.strftime("%Y-%m-%dT%H:%M:%S+02:00")
            param = urllib.parse.urlencode(
                {"start_date": start, "end_date": end}).replace("%3A", ":")
            response = requests.get(
                url,
                headers={
                    'Authorization': f'{self.token_type} {self.access_token}'},
                params=param)

        # Si on obtient bien un résultat json
        if response.status_code == 200 \
            and 'application/json' in response.headers.get(
                'Content-Type', ''):
            return response.json()
        else:
            return response.status_code

    def get_mean_hour_by_hour(self,
                              start_date: Optional[datetime.datetime] = None,
                              end_date: Optional[datetime.datetime] = None,
                              sandbox=False):
        """
        Récupère la moyenne de production de toutes les entités heure par heure

        :param start_date: Date de départ des datas
        :param end_date: Date de fin des datas
        :param sandbox: S'il faut utiliser l'URL sandbox pour les tests
        """

        if start_date is None or end_date is None or sandbox:
            data = self.get_per_unit(sandbox=sandbox)

            # Parfois l'appel à l'API peut résulter en erreur
            if not isinstance(data, dict):
                print("Erreur lors de l'appel à l'API")
                return None

            data = data.get("actual_generations_per_unit")
            return pd.json_normalize(data, record_path=['values']).groupby(
                'start_date')["value"].sum()

        delta = end_date - start_date
        data_days = {}

        # On récupère les données de l'API jour par jour car un trop
        # gros interval générère un plantage
        for i in range(delta.days + 1):
            day_start: datetime.datetime
            day_end: datetime.datetime

            day_start = start_date + datetime.timedelta(days=i)
            day_end = day_start + datetime.timedelta(hours=23)

            data = self.get_per_unit(
                day_start,
                day_end +
                datetime.timedelta(
                    days=1))

            # Parfois l'appel à l'API peut résulter en erreur
            if not isinstance(data, dict):
                print("Erreur lors de l'appel à l'API")
                return None

            data = data.get("actual_generations_per_unit")

            # On va traiter la donnée afin de récupérer le total de production
            # sur un temps donné
            data = pd.json_normalize(data, record_path=['values']).groupby(
                'start_date')["value"].sum()
            data_days[day_start.date()] = pd.Series(data)

        return data_days

    def get_token(self):
        """
        Permet de récupérer les tokens d'authentification
        """

        response = requests.post(
            config.URL_AUTH,
            headers={
                "content-type": f"application/x-www-form-urlencoded",
                "Authorization": f"Basic {config.SECRET_KEY}"})
        if response.ok:
            access_token = response.json()['access_token']
            token_type = response.json()['token_type']
        else:
            print("Impossible de se connecter")
            access_token = None
            token_type = None

        return token_type, access_token
