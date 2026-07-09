import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SendRequest:
    def __init__(self, url):
        if not url:
            raise ValueError("URL is not provided to send request")

        self.url = url

    def get(self, timeout=10):
        try:
            response = requests.get(
                self.url,
                timeout=timeout,
            )

            response.raise_for_status()

            return response.text

        except requests.exceptions.RequestException as error:
            raise RuntimeError(
                f"Failed to send request to {self.url}: {error}"
            )