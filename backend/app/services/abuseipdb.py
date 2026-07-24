import os
import requests

API_KEY = os.getenv("ABUSEIPDB_API_KEY")

URL = "https://api.abuseipdb.com/api/v2/check"


def check_ip(ip_address: str):
    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": 90
    }

    response = requests.get(
        URL,
        headers=headers,
        params=params
    )

    return response.json()