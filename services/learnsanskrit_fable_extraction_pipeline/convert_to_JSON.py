import json
from bs4 import BeautifulSoup


class ExtractDataFromLearnSanskrit:
    """Given raw data this class extracts all the required files from the data provided
    NOTE: Specific to learnsanskrit.cc page
    """

    def __init__(self, data):
        
        if not data:
            raise ValueError("DATA IS NOT PROVIDED TO CONVERT TO JSON")
        self.data = self._parse_json(data)
        

    def _parse_json(self,data):
        """Parsing the input json data"""
        try:
            if isinstance (data,(dict,list)):
                return data
            
            return json.loads(data)
        
        except(ValueError,TypeError):
            raise ValueError("INVALID JSON DATA")
        

       
    def _extract_english_title(self):
        """Extracting English Title from fable"""
        title_data = self.data['data']['summary_head']
        return title_data[0]
    
    def _extract_actors(self):
        """Extracting Actor Names"""
        title = self._extract_english_title()
        title.replace(" ","")
        return title.split(", ")
    

    def _extract_moral(self):
        title_data = self.data['data']['summary_head']
        story_moral = title_data[1]
        story_moral = story_moral.replace("(", "").replace(")", "")
        return story_moral
    
    def _extract_english_version_story(self):
        """Extracting english version story"""
        return self.data['data']['summary_text']
    
    
    def _extract_sanskrit_version_story(self):
        """Extracting Transliterd version"""
        sanskrit_version =[]
        sanskrit_texts = self.data["data"]["textsdeva"]
        
        for section in sanskrit_texts:
            
            soup = BeautifulSoup(section,"html.parser")
            divs = soup.find_all("div")
            
            words =[]
            
            for div in divs:
                data = div.get_text(strip=True)
                data = data.replace("\n","").replace("\\","")
                
                
                if data == "":
                    continue
                
                if data.isdigit():
                    continue
                
                words.append(data)
                
            if words:
                sanskrit_version.append(" ".join(words))
            
        
        return sanskrit_version
    
    def _extracting_sanskrit_version_story_title(self):
        sanskrit_version = self._extract_sanskrit_version_story()
        return sanskrit_version[0]
    
    
    def get_json_data(self):
        return {
            "title": {
                "englishVersion": self._extract_english_title(),
                "sanskritVersion": self._extracting_sanskrit_version_story_title()
            },
            "actors": self._extract_actors(),
            "storyMoral": [self._extract_moral()],
            "englishVersion": self._extract_english_version_story(),
            "sanskritVersion": self._extract_sanskrit_version_story()
        }
        
        
        
        