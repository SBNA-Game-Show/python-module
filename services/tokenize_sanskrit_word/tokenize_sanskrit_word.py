import requests
import uuid
import json
import re

class TokenizeSanskritWord:

    def __init__(self, word):

        self.word = word
        self.url = "https://dharmamitra.org/bff/api/translation"

        if not self.is_devanagari(word) and not self.is_iast(word):
            raise ValueError(
                f"Unsupported Sanskrit script: {word}"
            )


    def is_devanagari(self, text):
        """
        Checks if text contains Devanagari characters
        """
        return bool(
            re.search(r'[\u0900-\u097F]', text)
        )


    def is_iast(self, text):
        """
        Checks if text contains IAST transliteration characters
        """
        iast_chars = (
            "āīūṛṝḷḹṅñṭḍṇśṣ"
            "ĀĪŪṚṜḶḸṄÑṬḌṆŚṢ"
        )

        return any(char in text for char in iast_chars) or text.isascii()


    def tokenize(self):
        
        headers = self._create_headers()
        payload = self._create_payload(self.word)
        response = self._send_request(self.url,payload,headers)
        raw_data = self._extract_data(response)
        return self.word
    
    
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