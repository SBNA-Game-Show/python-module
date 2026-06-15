import nltk
from nltk.corpus import wordnet

class ExtractDefinitions:
    def __init__(self, data):
        self.data = data
    
    
    def _extract_data(self,data):
        return data.get("tokenized_english_version",[])
    
    
    def execute(self):
        tokens = self._extract_data(self.data)
        
        tokenized_with_definitions =[]
        
        for item in tokens:
            word = item.get("lemma","")
            synsets = wordnet.synsets(word)
            
            new_item = item.copy()
            
            new_item["definition"]=(synsets[0].definition() if synsets else None)
            
            tokenized_with_definitions.append(new_item)
            
        new_data = self.data.copy()
        new_data["tokenized_english_version"] = tokenized_with_definitions
        
        return new_data
        
        