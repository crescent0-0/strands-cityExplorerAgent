import requests
from .config import REQUEST_TIMEOUT, REQUEST_RETRIES

def get_json(url: str, params: dict | None = None, headers: dict | None = None) -> dict:
    for i in range(REQUEST_RETRIES + 1):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if i == REQUEST_RETRIES - 1:
                raise e
            continue

