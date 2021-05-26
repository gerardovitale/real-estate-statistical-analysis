import base64
import json
import os
from typing import Tuple
import urllib

import dotenv
import requests

from idealista.resources.SearchParams import SearchParams
from idealista.resources.SearchParamsBuilder import SearchParamsBuilder


def get_env_variables() -> Tuple[str, str]:
    dotenv.load_dotenv('.env')
    apikey = os.getenv("APIKEY")
    secret = os.getenv("SECRET")
    return apikey, secret


def get_oauth_token() -> str:
    url = "https://api.idealista.com/oauth/token"
    apikey, secret = get_env_variables()
    auth_bytes = base64.b64encode(f'{apikey}:{secret}'.encode('ascii'))
    auth = auth_bytes.decode('ascii')
    params = urllib.parse.urlencode({'grant_type': 'client_credentials'})
    headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 
               'Authorization': 'Basic ' + auth}
    response = requests.post(url, headers=headers, params=params)
    token = json.loads(response.text)['access_token']
    return token 


def set_search_params() -> SearchParams:
    builder = SearchParamsBuilder()
    builder.create_search_params
    builder.set_operation('sale')\
        .set_propertyType('homes')\
        .set_center('40.430,-3.702')\
        .set_locale('en')\
        .set_distance('10500')
    return builder._search_params


def get_search(token, search_params: SearchParams) -> str:
    url = "https://api.idealista.com/3.5/es/search"
    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, headers=headers, params=search_params.params)
    result = json.loads(response.text)
    return result
