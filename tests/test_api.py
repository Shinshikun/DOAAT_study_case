import datetime
import pandas as pd
import api.api

test_api = api.api.ActualGeneration()

def test_get_token():
    token_type, access_type = test_api.get_token()
    assert token_type is not None, "Authentification échouée"
    assert access_type is not None, "Authentification échouée"

def test_get_per_unit():

    response = test_api.get_per_unit(sandbox=True)
    assert type(response) == dict
    assert "actual_generations_per_unit" in response.keys()

def test_get_mean_hour_by_hour():
    
    # On test qu'on obtient bien une série pandas en utilisant sandbox
    response = test_api.get_mean_hour_by_hour(sandbox=True)
    assert type(response) == pd.Series

    # On test en récupérant une journée entière
    start = datetime.datetime(2023,1,1,0,0)
    end = datetime.datetime(2023,1,1,23,0)
    response = test_api.get_mean_hour_by_hour(start, end)
    assert type(response) ==  dict

    # On vérifie qu'on obtient bien 24 entrées correspondant aux 24 heures.
    assert len(list(response.keys())) == 1
    assert len(response[list(response.keys())[0]]) == 24

    # On test en récupérant deux journées
    start = datetime.datetime(2023,1,1,0,0)
    end = datetime.datetime(2023,1,2,0,0)
    response = test_api.get_mean_hour_by_hour(start, end)
    assert type(response) ==  dict

    # On vérifie qu'on obtient bien 48 entrées correspondant aux 48 heures.
    assert len(list(response.keys())) == 2
    assert len(response[list(response.keys())[0]]) + len(response[list(response.keys())[1]]) == 48
