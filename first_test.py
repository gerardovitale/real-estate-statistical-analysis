import json
from idealista.idealista_api import (get_oauth_token, get_search,
                                     set_search_params)

token = get_oauth_token()
search_params = set_search_params()
response = get_search(token, search_params)

with open('test_output.json', 'w') as json_file:
    json_file.write(json.dumps(response))