import requests

class GenericERPClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def create_sales_order(self, payload: dict):
        r = requests.post(f"{self.base_url}/sales-orders", json=payload, headers=self._headers(), timeout=30)
        r.raise_for_status()
        return r.json()

    def create_financial_entry(self, payload: dict):
        r = requests.post(f"{self.base_url}/financial-entries", json=payload, headers=self._headers(), timeout=30)
        r.raise_for_status()
        return r.json()
