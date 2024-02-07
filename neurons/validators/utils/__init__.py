
from typing import List
import torch
import random
import requests
import os
import bittensor as bt

EXPECTED_ACCESS_KEY = os.environ.get('EXPECTED_ACCESS_KEY', 'hello')
URL_SUBNET_18 = os.environ.get('URL_SUBNET_18')

def call_to_subnet_18_scoring(data):
    headers = {
        "access-key": EXPECTED_ACCESS_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(url=f"{URL_SUBNET_18}/scoring/", 
                             headers=headers, 
                             json=data)  # Using json parameter to automatically set the content-type to application/json

    if response.status_code in [401, 403]:
        bt.logging.error(f"Connection issue with Subnet 18: {response.text}")
        # os._exit(1)
    return response