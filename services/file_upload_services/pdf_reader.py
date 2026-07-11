import os
import re
import unicodedata

import fitz as pymupdf
from uuid import uuid4


from repository.learnsanskrit_metadata_repo import WriteTokenizedStoryToMongoDB
from services.tokenize_english_passage import TokenizeEnglishVersion
from services.tokenize_sanskrit_passage_web import TokenizeSanskritPassageWeb
from services.clean_tokenized_english_words_array import CleanEnglishTokenizedData
from services.extract_definitions_english_words import ExtractDefinitions
from services.extract_english_synonym_antonym import ExtractEnglishSynonymAntonym



class PDFReader:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR,"..", "data")

    def __init__(self, file_name):
        if not file_name:
            raise ValueError("File name was not provided.")

        self.file_name = file_name
        self.file_path = os.path.join(self.DATA_DIR, self.file_name)

        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"PDF not found: {self.file_path}")

        self.DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")
        self.LATIN_RE = re.compile(r"[A-Za-z]")
        self.TITLE_RE = re.compile(r"^(?:[0-9]+|[०-९]+)[\.\)]\s*(.+)$")
        
        
    def execute(self):
        with self._open_pdf() as doc:
        
            stories =[]
            
            current={
                "title":None,
                "english":[],
                "sanskrit":[]
            }
            
            waiting_for_content = False
            
            def save_story():
                if current["title"] or current["sanskrit"]:
                    stories.append({
                        "title":current["title"],
                        "english":" ".join(current["english"]),
                        "sanskrit":" ".join(current["sanskrit"])
                    })
                    
            for page in doc:
                lines=[
                    self._clean_data(x)
                    for x in page.get_text("text").splitlines()
                    if self._clean_data(x)
                ]
                
                for line in lines:
                    if line == "Automatic Zoom":
                        continue
                    
                    title = self._extract_title(line)
                    
                    if title:
                        # First Title
                        if current["title"] is None:
                            current["title"]= title
                            waiting_for_content = True
                            continue
                        # Second Title of same story
                        if(waiting_for_content
                        and not current["english"]
                        and not current["sanskrit"]
                        ):
                            continue
                        
                        save_story()
                        
                        current ={
                            "title":title,
                            "english":[],
                            "sanskrit":[]
                        }
                        
                        waiting_for_content = True
                        continue
                    
                    lang = self._detect_language(line)
                    
                    if lang == "english":
                        current["english"].append(line)
                        waiting_for_content = False
                        
                    elif lang == "sanskrit":
                        current["sanskrit"].append(line)
                        waiting_for_content = False
                        
            save_story()
            
            merged_stories = self._merge_stories(stories)
            
            results_array = []
            
            for story in merged_stories:
                eng_tokenized = self._tokenize_english_passage(story)
                synonym_added = self._add_definitions(eng_tokenized)
                definitions_added = self._add_definitions(synonym_added)
                clean_eng_passage = self._clean_english_tokenized(definitions_added)
                sa_tokenized = self._tokenize_sanskrit_passage(clean_eng_passage)
                
                result = self._write_to_DB(sa_tokenized)
                results_array.append(result)
                
            if all(
                result.endswith("added to DB")
                for result in results_array
            ):
                return{
                    "success":True,
                    "message": f"{len(results_array)} stores Tokenized and Added to DB"
                }        
        return {
            "success":False,
            "message": "Some Stories Failed to tokenize or added to DB",
            "results": results_array
        }      


    def _open_pdf(self):
        return pymupdf.open(self.file_path)   

    def _clean_data(self, text):
        text = unicodedata.normalize("NFKC", text)
        text = text.replace("\u200c", "").replace("\u200d", "")
        return re.sub(r"\s+", " ", text).strip()

    def _detect_language(self, text):
        devanagari = len(self.DEVANAGARI_RE.findall(text))
        latin = len(self.LATIN_RE.findall(text))

        if devanagari > latin:
            return "sanskrit"
        elif latin > devanagari:
            return "english"

        return "unknown"

    def _extract_title(self, line):
        match = self.TITLE_RE.match(line)

        if not match:
            return None

        title = match.group(1).strip()

        # Ignore long numbered paragraphs
        if len(title.split()) > 10:
            return None

        # Ignore sentence-like titles
        if title.endswith((".", "।", ":", ",")):
            return None

        return title
    
    def _merge_stories(self, stories):
        merged = []
        i = 0

        while i < len(stories):
            current = stories[i]

            if i + 1 < len(stories):
                nxt = stories[i + 1]

                if (
                    current["sanskrit"]
                    and not current["english"]
                    and nxt["english"]
                    and not nxt["sanskrit"]
                ):
                    merged.append({
                        "_id": str(uuid4()),
                        "title": {
                            "englishTitle": nxt["title"],
                            "sanskritTitle": current["title"]
                        },
                        "englishVersion": nxt["english"],
                        "sanskritVersion": [current["sanskrit"]]
                    })
                    i += 2
                    continue

                if (
                    current["english"]
                    and not current["sanskrit"]
                    and nxt["sanskrit"]
                    and not nxt["english"]
                ):
                    merged.append({
                        "_id": str(uuid4()),
                        "title": {
                            "englishTitle": current["title"],
                            "sanskritTitle": nxt["title"]
                        },
                        "englishVersion": current["english"],
                        "sanskritVersion": [nxt["sanskrit"]]
                    })
                    i += 2
                    continue

            # Always keep the current story if it wasn't merged
            merged.append(current)
            i += 1

        return merged
    
    def _tokenize_english_passage(self,data):
        request = TokenizeEnglishVersion(data)
        return request.tokenize_english_version()
    
    def _add_synonyms(self,data):
        request = ExtractEnglishSynonymAntonym(data)
        return request.execute()
    
    def _add_definitions(self,data):
        request = ExtractDefinitions(data)
        return request.execute()
    
    def _clean_english_tokenized(self,data):
        request = CleanEnglishTokenizedData(data)
        return request.execute()
    
    def _tokenize_sanskrit_passage(self,data):
        request = TokenizeSanskritPassageWeb(data)
        return request.tokenize()
    
    def _write_to_DB(self,data):
        writer = WriteTokenizedStoryToMongoDB(data)
        return writer.save_story()
    
    
    
    

            