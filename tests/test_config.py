import requests

import api.config as config

def test_auth():
    response = requests.post(config.URL_AUTH, 
                                headers={"content-type": f"application/x-www-form-urlencoded", 
                                        "Authorization": f"Basic {config.SECRET_KEY}"}
                            )
    assert response.ok == True
    assert response.status_code == 200

    if response.ok:
        print("Authentification réussie !")
    else:
        print("Authentification échouée.")
        print(f"Status : {response.status_code}")
        print(f"Raison : {response.reason}")
