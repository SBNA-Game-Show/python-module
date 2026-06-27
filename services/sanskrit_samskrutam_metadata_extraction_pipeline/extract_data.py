from bs4 import BeautifulSoup
import requests
class RetrieveRawData:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml",
            "Referer": "https://sanskrit.samskrutam.com/"
        }

        self.data = self.get_data()   # store result

    def get_data(self):
        raw_data = self._send_Request(self.url)
        data = self._get_data(raw_data)
        return data

    def _send_Request(self, url):
        session = requests.Session()
        session.headers.update(self.headers)

        response = session.get(url)
        response.raise_for_status()

        return response.text          # return HTML string

    def _get_data(self, raw_html):
        soup = BeautifulSoup(raw_html, "html.parser")
        return soup.find("div", id="PageContentDiv")
      
        