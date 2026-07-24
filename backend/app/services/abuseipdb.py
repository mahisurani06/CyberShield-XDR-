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

    data = response.json()["data"]

    score = data["abuseConfidenceScore"]

    if score >= 80:
        risk = "Malicious"
        recommendation = "Block this IP immediately."
    elif score >= 30:
        risk = "Suspicious"
        recommendation = "Investigate before allowing communication."
    else:
        risk = "Safe"
        recommendation = "No immediate action required."

    return {
        "ip_address": data["ipAddress"],
        "risk_score": score,
        "risk_level": risk,
        "country": data["countryCode"],
        "isp": data["isp"],
        "domain": data["domain"],
        "usage_type": data["usageType"],
        "is_tor": data["isTor"],
        "reports": data["totalReports"],
        "recommendation": recommendation
    }