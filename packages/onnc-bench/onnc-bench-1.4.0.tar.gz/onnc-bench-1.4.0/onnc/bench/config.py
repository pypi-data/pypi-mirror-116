import os
from os.path import expanduser
import requests

try:
    if int(os.environ['ONNC_TESTMODE']):
        api_host = 'http://127.0.0.1:8000'
except KeyError:
    api_host = 'https://api.onnc.skymizer.com'

onnc_key_var = 'ONNC_APIKEY'


def verify_key(api_key: str) -> bool:
    """Verify API Key

    :param api_key: Your API key str
    :type api_key: str
    :return: Indicate if the key is valid
    :rtype: bool

    """

    response = requests.post(f"{api_host}/api/v1/api_key/{api_key}/")
    return response.json()["success"]


def get_device_list():
    """Get Supported Devices

    :return: Supported devices
    :rtype: dict

    """
    response = requests.get(f"{api_host}/api/v1/supprted/devices/")
    response = response.json()
    if ("success" in response) and (response["success"]):
        return response["payload"]


def get_bench_templates():
    """Get Supported Templates for onnc-create

    :return: Supported templates
    :rtype: dict

    """
    response = requests.get(f"{api_host}/api/v1/supprted/bench/")
    response = response.json()
    if ("success" in response) and (response["success"]):
        return response["payload"]
