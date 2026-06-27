import requests
import re
from bs4 import BeautifulSoup

class ExtractData:
    def __init__(self, url, vendorId):
        if url is None or vendorId is None:
            raise ValueError("URL & VENDOR ID BOTH ARE REQUIRED")

        self.url = url
        self.vendorId = vendorId
        self.headers = {
                        "User-Agent": "Mozilla/5.0",
                        "Accept": "text/html,application/xhtml+xml",
                        "Referer": "https://sanskrit.samskrutam.com/"
                        }
        
        
        
    def execute(self):
        
        complete_data = self._send_request(self.url,self.headers)
        raw_data = self._get_fable(complete_data,self.vendorId)
        clean_data = self.clean_html(raw_data)
        
        return clean_data
        
        
        
    def _send_request(self,url,headers):
        session = requests.Session()
        session.headers.update(headers)
        raw_html = session.get(url)
        text = raw_html.text
        
        return text
    
    def _get_fable(self,data,vendorId):
        soup = BeautifulSoup(data,"html.parser")
        request = soup.find("a",{"name": vendorId})
        data = request.find_parent("p")
        
        return data
    
    def clean_html(self,p_tag):
        for tag in p_tag(["hr"]):
            tag.decompose()

        for br in p_tag.find_all("br"):
            br.replace_with("\n")

        text = p_tag.get_text("\n", strip=True)

        # normalize blank lines
        text = re.sub(r"\n\s*\n+", "\n\n", text).strip()

        return text
        