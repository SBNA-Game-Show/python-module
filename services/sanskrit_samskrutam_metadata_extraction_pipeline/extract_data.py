from bs4 import BeautifulSoup
import requests
import time
import json
from uuid import uuid4
from datetime import datetime

class RetrieveMetaData:
    def __init__(self):
        self.url_block1 = "https://sanskrit.samskrutam.com/en.literature-stories-01.ashx"
        self.url_block2 = "https://sanskrit.samskrutam.com/en.literature-stories-02.ashx"
        self.headers = {
                "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml",
    "Referer": "https://sanskrit.samskrutam.com/"
        }
        
        
    def _send_Request(self,url):
        session = requests.Session()
        session.headers.update(self.headers)
        
        text = session.get(url)
        
        return text
    
    def _get_data(self, raw_data):
        soup = BeautifulSoup(raw_data,"html.parser")
        data = soup.find("div",id="PageContentDiv")
        
        return data
    
    def _parse_data(self, data):
        
        