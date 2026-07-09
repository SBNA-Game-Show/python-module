from services.gurukula.meta_data.send_request import SendRequest
from bs4 import BeautifulSoup


class ExtractCategory:
    def __init__(self):
        self.url = "https://gurukula.com/sa"
        
        
    def extract(self):
        
        raw_data = self._send_request(self.url)
        raw_tags = self._parse_data(raw_data)
        categories = self._extract_categories(raw_tags)
        return categories
    
    def _send_request(self,url):
        req = SendRequest(url)
        return req.get()
    
    def _parse_data(self,data):
        soup = BeautifulSoup(data,"html.parser")
        raw_tags = soup.find_all("div",class_="all-epics-card")
        
        return raw_tags
    
    def _extract_categories(self,data):
        categories=[]
        
        for cat in data:
            link = cat.find("a", href=True)
            name = cat.find("div", class_="epic-name")
            
            if link and name:
                categories.append({
                    "category":name.get_text(strip =True),
                    "category_link": link["href"]
                })
                
        return categories
                