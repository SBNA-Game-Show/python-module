import requests
import uuid
import json



from utils.dharmamitra_parser import DharmamitraExtractor
from utils.sanskrit_parser import TransliterateToSanskrit,SanskritToTransliterate

class TokenizeSanskritPassageWeb:
    def __init__(self, data):
        if not data:
            raise ValueError("Data is not provided to Tokenize Sanskrit Passage.")
        
        self.data = data
        self.url = "https://dharmamitra.org/bff/api/translation"
        self.parser = DharmamitraExtractor()
        
        
        
    def tokenize(self):
        
        sa_passage = self._extract_sanskrit_passage(self.data)
        payload_data = self._normalize_passage(sa_passage)
        payload = self._create_payload(payload_data)
        headers = self._create_headers()
        response = self._send_request(self.url,payload,headers)
        if response.status_code != 200:
            raise RuntimeError(f"Request failed with status code {response.status_code}: {response.text}")
        
        raw_data = self._extract_data(response)
        
        tokenized_data = self.parser.extract(raw_data)
        cleaned_data = self._remove_duplicates(tokenized_data)
        normalized_data = self._convert_to_devnagari(cleaned_data)
        
        
        new_data = self.data.copy()
        new_data["tokenized_sanskrit_version"] = normalized_data
        
        
        return new_data
        
        
            
        
        
    
    
    def _extract_sanskrit_passage(self,data):
        return data.get("sanskritVersion", [])
    
    def _normalize_passage(self,passage):
        
        cleaned_passage =[]
        
        for sentence in passage:
                sentence = sentence.replace("|", "")
                sentence = sentence.replace("||", "")
                sentence = sentence.replace("-", "")
                sentence = sentence.replace("–", "")
                sentence = sentence.replace("—", "")
                sentence = sentence.replace('"', "")
                sentence = sentence.replace("“", "")
                sentence = sentence.replace("”", "")
                sentence = sentence.replace(",", "")
                sentence = sentence.replace(".", "")
                sentence = sentence.replace("?", "")
                sentence = sentence.replace("!", "")
                sentence = sentence.replace(";", "")
                sentence = sentence.replace(":", "")
                sentence = sentence.replace("(", "")
                sentence = sentence.replace(")", "")
                
                cleaned_passage.append(sentence)
                
        payload_data = "\n".join(cleaned_passage)
        
        return payload_data
    
    def _create_payload(self,data):
        return{
                "do_grammar": False,
                "input_encoding": "auto",
                "input_sentence": data,
                "messages": [
                    {
                        "parts": [
                            {
                                "type": "text",
                                "text": data
                            }
                        ],
                        "id": str(uuid.uuid4()),
                        "role": "user"
                    }
                ],
                "mode": "explain-grammar",
                "target_lang": "english"
            
        }
        
    def _create_headers(self):
        return{
                "Accept": "text/event-stream",
                "Content-Type": "application/json",
                "Origin": "https://dharmamitra.org",
                "Referer": "https://dharmamitra.org/"
        }
            
            
        
    def _send_request(self,url,payload,headers):
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            stream=True
            
        )
        
        return response
    
    def _extract_data(self, response):
        full_text = ""

        for line in response.iter_lines():
            if not line:
                continue

            line = line.decode("utf-8")

            if line.startswith("data: "):
                event_data = line[6:]

                if event_data == "[DONE]":
                    break

                try:
                    obj = json.loads(event_data)
                except json.JSONDecodeError:
                    continue

                if obj.get("type") == "text-delta":
                    full_text += obj.get("delta", "")

        return full_text
    
    def _remove_duplicates(self,data):
        cleaned_array =[]
        unique_words = set()
        
        for item in data:
            word = item["text"]
            
        if word not in unique_words:
            unique_words.add(word)
            cleaned_array.append(item)
            

        return cleaned_array
    
    def _convert_to_devnagari(self,data):
        final_array =[]
        
        for item in data:
            text = item["text"]
            lemma = item["lemma"]
            
        text_converter = TransliterateToSanskrit(text)
        devanagari_text = text_converter.translate()
        
        lemma_converter = TransliterateToSanskrit(lemma)
        devanagari_lemma = lemma_converter.translate()
        
        final_array.append({
            "text":devanagari_text,
            "lemma": devanagari_lemma,
            "upos":item["upos"],
            "features":item["features"],
            "definition":item["definition"]
        })
        
        return final_array
    
    
