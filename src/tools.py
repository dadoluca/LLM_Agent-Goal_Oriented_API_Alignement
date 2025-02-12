# function to retreave the readme and the swagger APIs
import requests
import json 

from src.data_model import API

def get_markdown(link: str):
    res = requests.get(url=link)
    return res.text


def get_api_list_from_swagger():
    api_list = get_markdown("https://raw.githubusercontent.com/WebFuzzing/EMB/refs/heads/master/openapi-swagger/genome-nexus.json")

    json_api_list = json.loads(api_list)["paths"]
    api_paths = json_api_list.keys()

    preprocessed_api_list = []

    for api in api_paths:
        path = json_api_list[api]
        for method in path.keys():
            preprocessed_api_list.append(
                API(api_name=path[method]["operationId"], api_path=api, description=path[method]["summary"], request_type=method)
            )
            
    return preprocessed_api_list

def api_list_to_string(api_list):
    apis = ""
    for api in api_list:
        apis += api.api_name + ", "
    # Remove the trailing comma and add a newline
    apis = apis.rstrip(", ") + "\n"
    return apis