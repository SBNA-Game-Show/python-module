from services.sanskrit_samskrutam_fable_extraction_pipeline.extract_data import ExtractData
from services.sanskrit_samskrutam_fable_extraction_pipeline.convert_to_JSON import NormalizeData
from repository.sanskrit_samskrutam_metadata_repo import GetStoryDataById
from services.tokenize_english_passage import TokenizeEnglishVersion
from services.tokenize_sanskrit_passage_web import TokenizeSanskritPassageWeb
from services.extract_english_synonym_antonym import ExtractEnglishSynonymAntonym
from services.extract_definitions_english_words import ExtractDefinitions
from services.clean_tokenized_english_words_array import CleanEnglishTokenizedData
from repository.learnsanskrit_metadata_repo import WriteTokenizedStoryToMongoDB
from repository.sanskrit_samskrutam_metadata_repo import UpdateStoryToUsed


class ExtractNewFable:
    def __init__(self,storyId):
        if storyId is None:
            raise ValueError("STORY ID IS REQUIRED")
        
        self.storyId = storyId
        
        
    def execute(self):
        ## 1. Get vendor id and web link from meta data
        
        meta_data = self._get_story_data(self.storyId)        
        vendorId = meta_data["vendorId"]
        url = meta_data["source_url"]        
        ## 2. Send request to sanskrit.samskrutam to fetch data
        data = self._send_request(url,vendorId)       
        ## 3. Normalize data
        data = self._normalize_data(data)
        ## 4. Tokenize English Passage
        data = self._tokenize_english_version(data)
        ## 5. Tokenize Sanskrit Passage
        data = self._tokenize_sanskrit_version(data)
        ## 6. Add synonyms and Antonyms for tokenized english
        data = self._add_english_grammar(data)
        ## 7. Add english definitions to the tokenized english
        data = self._add_english_definitions(data)
        ## 7. Clean English Tokenized Array
        data = self._clean_eng_data(data)
        data["_id"] = self.storyId
        ##8. Write to Mongo DB
        result = self._write_to_db(data)
        
        if result is None:
            return "Internal Server Error"
        
        import gc
        gc.collect()
        
        updater = self._update_meta_data(self.storyId)
     
        
        return {
            "success": True,
            "message": "Story Downloaded Successfully"
        }
    
    def _get_story_data(self, storyId):
        req = GetStoryDataById(storyId)
        return req.get_data()
    
    def _send_request(self,url,vendorId):
        req = ExtractData(url,vendorId)
        return req.execute()
    
    def _normalize_data(self,data):
        req = NormalizeData(data)
        return req.execute()
    
    def _tokenize_english_version(self,data):
        req = TokenizeEnglishVersion(data)
        return req.tokenize_english_version()
    
    def _tokenize_sanskrit_version(self,data):
        req = TokenizeSanskritPassageWeb(data)
        return req.tokenize()
    
    def _add_english_grammar(self,data):
        req = ExtractEnglishSynonymAntonym(data)
        return req.execute()
    
    def _add_english_definitions(self,data):
        req = ExtractDefinitions(data)
        return req.execute()
    
    
    def _clean_eng_data(self,data):
        req = CleanEnglishTokenizedData(data)
        return req.execute()
    
    def _write_to_db(self,data):
        req = WriteTokenizedStoryToMongoDB(data)
        return req.save_story()
    
    def _update_meta_data(self,storyId):
        req = UpdateStoryToUsed(storyId)
        return req.update()
        
        
    
    
    
    
        