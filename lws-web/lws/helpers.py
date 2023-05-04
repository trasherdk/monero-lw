import requests

from lws import config


class LWS:
    def __init__(self, admin_key):
        self.admin_key = admin_key
    
    def list_accounts(self):
        endpoint = f"{config.LWS_ADMIN_URL}/list_accounts"
        data = {"auth": self.admin_key}
        try:
            req = requests.post(endpoint, json=data, timeout=5)
            req.raise_for_status()
            if req.ok:
                return req.json()
            return {}
        except Exception as e:
            print(f"Failed to list accounts: {e}")
            return {}
