from bs4 import BeautifulSoup
from services.gurukula.meta_data.send_request import SendRequest


class ExtractStoryList:
    def __init__(self, categoryURL):
        if not categoryURL:
            raise ValueError("Category URL Is not Provided to Extract Story List")
        self.base_url = "https://gurukula.com"
        self.url = self.base_url+categoryURL
        
        
    def execute(self):
        raw_data = self._send_request(self.url)
        parsed_data = self._parse_data(raw_data)
        stories_list = self._extract_story_list(parsed_data)
        
        return stories_list        
        
        
        
    def _send_request(self,url):
        query = SendRequest(url)
        result = query.get()
        
        return result
    
    def _parse_data(self,data):
        soup = BeautifulSoup(data,"html.parser")
        raw_tags = soup.find_all("div", class_="box")
        return raw_tags
    
    def _extract_story_list(self,data):
        stories_list =[]
        
        for tags in data:
            link = tags.select_one(".heading a")
            
            if link:
                stories_list.append({
                    "url":link.get("href"),
                    "text":link.get_text(strip=True)
                })
                
        return stories_list
        