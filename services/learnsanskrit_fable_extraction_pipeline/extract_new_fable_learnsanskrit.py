import re
from repository.file_system.get_stroy_data_by_id import GetStoryData
from repository.file_system.update_story_data_used import UpdateStoryDataUsedStatus
from utils.file_system_writer import WriteToFileSystem

from services.learnsanskrit_fable_extraction_pipeline.extract_data import RetrieveStoryFromLearnSanskrit
from services.learnsanskrit_fable_extraction_pipeline.convert_to_JSON import ExtractDataFromLearnSanskrit

from services.tokenize_english_passage import TokenizeEnglishVersion
from services.tokenize_sanskrit_passage import TokenizeSanskritVersion
from services.extract_english_synonym_antonym import ExtractEnglishSynonymAntonym
from services.extract_definitions_english_words import ExtractDefinitions

from repository.learnsanskrit_metadata_repo import WriteTokenizedStoryToMongoDB,UpdateLearnSanskritMetaData,GetMetaDataById
from services.clean_tokenized_english_words_array import CleanEnglishTokenizedData

class FetchNewFable:
    """Orchestrates the pipeline to fetch, clean, tokenize, and save a fable."""

    def __init__(self, story_id):
        self.story_id = story_id

    def execute(self):
        """Runs the complete execution pipeline for a given story ID."""
        

        
        # Fetching from DB
        story_data = self._get_story_data_from_DB(self.story_id)
        
        if not story_data:
            raise ValueError(f"No data found for the given ID: {self.story_id}")
            
        vendor_id = story_data.get("vendorId")
        
        if not vendor_id:
            raise ValueError("Vendor Id Mismatch")
        
        match = re.match(r"[a-zA-Z]+",vendor_id)
        
        if not match:
            raise ValueError(f"Invalid vendorId format: {vendor_id}")
        story_category = match.group()
        # 2. Extract & Transform
        raw_data = self._retrieve_raw_data(vendor_id)
        cleaned_data = self._clean_data(raw_data)
        ## Adding the same request id for the story
        cleaned_data["_id"] = self.story_id
        cleaned_data["category"] = story_category
        
        ## 3. Enrich / Tokenize
        # Tokenizing English words
        tokenized_english = self._tokenize_english_version(cleaned_data)
        #Adding Synonyms and antonyms
        tokenized_english_with_grammer = self._add_synonym_antonym(tokenized_english)
        definitions_added = self._add_definitions(tokenized_english_with_grammer)
        
        
        #Tokenizing Sanskrit words
        tokenized_sanskrit_version = self._tokenize_sanskrit_version(definitions_added)
        # cleaning english words that does not have synonyms and antonyms
        final_version = self._clean_english_data(tokenized_sanskrit_version)
        
        
        
        # writing to mongo db database
        result = self._write_to_mongoDB(final_version)
        
        if result is None:
            return "Internal server Error"
        
        # Updating Learn Sanskrit Metadata collection
        
        updater = self._update_story_toDB(self.story_id)
        
            
        return {
            "success": True,
            "message": "Fable downloaded successfully"
        }

    # Helper methods  
    
    def _retrieve_raw_data(self, vendor_id):
        return RetrieveStoryFromLearnSanskrit(vendor_id).send_request()
        
    def _clean_data(self, raw_data):
        return ExtractDataFromLearnSanskrit(raw_data).get_json_data()
        
    def _tokenize_english_version(self, cleaned_data):
        return TokenizeEnglishVersion(cleaned_data).tokenize_english_version()
    
    
    def _add_synonym_antonym(self, tokenized_english):
        return ExtractEnglishSynonymAntonym(tokenized_english).execute()
        
    def _tokenize_sanskrit_version(self, tokenized_english_with_grammar):
        return TokenizeSanskritVersion(tokenized_english_with_grammar).tokenize_sanskrit()
    
    def _write_to_mongoDB(self, story):
        writer = WriteTokenizedStoryToMongoDB(story)
        return writer.save_story()
    
    def _update_story_toDB(self, story_id):
        updater = UpdateLearnSanskritMetaData(story_id)
        return updater.update()
    
    def _get_story_data_from_DB(self,story_id):
        req = GetMetaDataById(story_id)
        result = req.get_data()
        print("DB RESULT:", result)
        return result
    
    def _clean_english_data(self,data):
        req = CleanEnglishTokenizedData(data)
        return req.execute()
    
    
    def _add_definitions(self,data):
        req = ExtractDefinitions(data)
        return req.execute()
    
    ## Writing to file System for testing purposes only
    def _get_story_data(self, story_id):
        return GetStoryData(story_id).response
    
    def _write_to_file_system(self, final_data):
        # FIXED: Wrapped in try-except to return a boolean result based on the writer's success
        try:
            WriteToFileSystem(self.file_name, final_data)
            return True
        except Exception as e:
            print(f"File writing error: {e}")
            return False
        
    def _update_story_status(self, story_id):
        updater = UpdateStoryDataUsedStatus(story_id)
        return updater.execute()