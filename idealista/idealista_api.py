import base64
import json
import os
import urllib
from datetime import date
from typing import Tuple

import dotenv
import jsonlines
import requests

from idealista.resources.decorators.time_it import time_it
from idealista.resources.searchParams.SearchParams import SearchParams
from idealista.resources.searchParams.SearchParamsBuilder import \
    SearchParamsBuilder



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
        .set_distance('10500')\
        .set_maxItems('50')\
        .set_numPage('1')
    return builder._search_params    


def get_response(token, search_params: SearchParams) -> dict:
    url = "https://api.idealista.com/3.5/es/search"
    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.post(url, headers=headers, params=search_params.params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise err
    result = json.loads(response.text)
    return result


def get_response_info() -> requests.Response:
    token = get_oauth_token()
    search_params = set_search_params()
    response = get_response(token, search_params)
    response.pop('elementList', None)
    return response


@time_it
def save_responses_as_jsonl(pages_to_iter: int) -> str:
    today = date.today().strftime("%d-%m-%Y")
    file_name = f'outputs/idealistaApiOutput{today}.jsonl'
    token = get_oauth_token()
    search_params = set_search_params()
    for page in range(1, pages_to_iter, 1):
        search_params.params['numPage'] = page
        response = get_response(token, search_params)
        with jsonlines.open(file_name, mode='a') as writer:
            writer.write_all(response['elementList'])
    return file_name
