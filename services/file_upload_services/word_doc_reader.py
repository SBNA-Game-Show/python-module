import re
import os
from docx import Document
from uuid import uuid4

from repository.learnsanskrit_metadata_repo import WriteTokenizedStoryToMongoDB
from services.tokenize_english_passage import TokenizeEnglishVersion
from services.tokenize_sanskrit_passage_web import TokenizeSanskritPassageWeb
from services.clean_tokenized_english_words_array import CleanEnglishTokenizedData
from services.extract_definitions_english_words import ExtractDefinitions
from services.extract_english_synonym_antonym import ExtractEnglishSynonymAntonym

class ReadWordDocument:
    
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR,"..", "data")
    
    def __init__(self, fileName):
        if not fileName:
            raise ValueError("File Name Not Provided to Read Word Document")
        self.fileName = fileName
        self.file_path = os.path.join(self.DATA_DIR,self.fileName)
        
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"Word Document Not Found: {self.file_path}")
        
        self.DEVANAGARI = re.compile(r'[\u0900-\u097F]')
        
        
    def execute(self):
        
        doc = Document(self.file_path)
        paragraphs = [
            p.text.strip()
            for p in doc.paragraphs if p.text.strip()
            ]
        stories =[]
        i = 0
        while i < len(paragraphs):
            # English Title
            english_title = paragraphs[i]
            i += 1
            # English Passage
            english_passage = []
            while i < len(paragraphs) and not self._is_sanskrit(paragraphs[i]):
                english_passage.append(paragraphs[i])
                i += 1
                
            #Sanskrit Title
            sanskrit_title = paragraphs[i]
            i += 1
            
            # Sanskrit Passage
            sanskrit_passage = []
            while i < len(paragraphs):
                if not self._is_sanskrit(paragraphs[i]):
                    break
                
                sanskrit_passage.append(paragraphs[i])
                i += 1
                
            stories.append({
                "_id": str(uuid4()),
                "title":{
                    "englishVersion": english_title,
                    "sanskritVersion":sanskrit_title
                },
                "englishVersion":" ".join(english_passage),
                "sanskritVersion":sanskrit_passage
                
            })
            
        results_array = [] 
        for story in stories:
            eng_tokenized = self._tokenize_english_passage(story)
            synonym_added = self._add_synonyms(eng_tokenized)
            definitions_added = self._add_definitions(synonym_added)
            clean_eng_passage = self._clean_english_tokenized(definitions_added)
            sa_tokenized = self._tokenize_sanskrit_passage(clean_eng_passage)
            
            result = self._write_to_DB(sa_tokenized)
            results_array.append(result)
            
        if all(
                result.endswith("added to DB")
                for result in results_array
            ):
                if os.path.exists(self.file_path):
                    os.remove(self.file_path)
                
                return{
                    "success":True,
                    "message":f"{len(results_array)} stories tokenized and added to DB"
                }
                
        if os.path.exists(self.file_path):
                os.remove(self.file_path)            
            
        return {
            "success": False,
            "message":"Some Stories Failed to tokenize or added to DB",
            "results": results_array
        }
    
    def _is_sanskrit(self,text):
        return bool(self.DEVANAGARI.search(text))
    
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
        
        