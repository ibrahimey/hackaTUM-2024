import requests


class AzureOpenAIClient:
    def __init__(self, endpoint: str, api_key: str) -> None:
        self.endpoint = endpoint
        self.headers = {
            "Content-Type": "application/json",
            "api-key": api_key,
        }

    def send_request(self, payload):
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")
        return response.json()["choices"][0]["message"]["content"]
