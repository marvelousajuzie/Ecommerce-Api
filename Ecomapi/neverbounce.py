import neverbounce_sdk as nb
import requests
import logging
from Ecommerce import settings


logger = logging.getLogger(__name__)
NEVERBOUNCE_URL = "https://api.neverbounce.com/v4/single/check"

def verify_email(email):
    payload = {
        'key': settings.NEVERBOUNCE_API_KEY,
        'email': email,
        'validation': 'extended'
    }
    response = requests.get(NEVERBOUNCE_URL, params=payload)
    result = response.json()
    if 'result' in result:
        return result['result'] == 'valid'
    else:
        print(f"NeverBounce API error: {result}")
        return False

