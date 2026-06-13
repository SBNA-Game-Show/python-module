

class CleanEnglishTokenizedData:
    
    def __init__(self, data):
        self.data = data


    def execute(self):
        
        tokenized_array = self._extract_tokenized_data(self.data)
        cleaned_version = self._remove_space_punctuation(tokenized_array)
        final_version = self._remove_empty_arrays(cleaned_version)
        duplicate_removed = self._remove_duplicates(final_version)
        
        new_data = self.data.copy()
        new_data["tokenized_english_version"] = duplicate_removed
        
        return new_data
        
        
        
        
    def  _extract_tokenized_data(self,data):
        return data.get("tokenized_english_version",[])
    
    
    def _remove_space_punctuation(self,tokenized_array):
        tokenized_array_copy = []
        for item in tokenized_array:
            # Skipping if the pos is space or punctuation
            if item.get("pos") in ["SPACE","PUNCT"]:
                continue
            
            # Copying the rest of data
            cleaned_item = item.copy()
            tokenized_array_copy.append(cleaned_item)
            
        return tokenized_array_copy
    
    def _remove_empty_arrays(self,cleaned_version):
        cleaned_version_copy =[]
        for item in cleaned_version:
            #creating an copy of the item
            cleaned_item = item.copy()
            
            #Finding all keys where the values are empty list
            
            empty_keys = [key for key, value in cleaned_item.items()if value == []]
            
            # Removing empty  synonyms and antonyms fields
            for key in empty_keys:
                cleaned_item.pop(key)
                
            # writing to cleaned_version_copy
            cleaned_version_copy.append(cleaned_item)
            
        return cleaned_version_copy
    
    def _remove_duplicates(self,data):
        seen = set()
        result =[]
        for item in data:
            word = item.get("text")
            if not word:
                continue
            
            key = word.lower().strip()
            
            if key in seen:
                continue
            
            seen.add(key)
            result.append(item)
            
        return result
        
            
            
        