from config.dbconfig import connect_db

from utils.tokenized_story_mapper import TokenizedStoryMapper
from pymongo.errors import BulkWriteError, PyMongoError


class LearnSanskritMetaDataRepository:

    def __init__(self):
        self.db = connect_db()
        self.collection = self.db["learnsank_meta"]

    def save_many(self, docs: list) -> dict:

        if not isinstance(docs, list):
            raise TypeError("docs must be a list of documents")

        if len(docs) == 0:
            raise ValueError("No documents provided to insert")

        try:
            result = self.collection.insert_many(docs)

            return result
        
        
        except BulkWriteError as e:
            return {
                "message": "Bulk write error occurred",
                "error": str(e.details)
            }

        except PyMongoError as e:
            return {
                "message": "Database error occurred",
                "error": str(e)
            }


class WriteTokenizedStoryToMongoDB:
    def __init__(self, story_data):
        self.data = story_data
        self.db = connect_db()
        self.collection = self.db["tokenized_stories"]
        
    def save_story(self):
        doc = TokenizedStoryMapper.to_schema(self.data)
        
        result = self.collection.insert_one(doc)
        
        return f"{result.inserted_id} tokenized and added to DB"
 
class UpdateLearnSanskritMetaData:

    def __init__(self, story_id):
        self.story_id = story_id
        self.db = connect_db()
        self.collection = self.db["learnsank_meta"]

    def update(self):

        result = self.collection.update_one(
            {"story_description._id": self.story_id},
            {"$set": {"story_description.$.used": True}},
        )

        if result.modified_count == 0:
            raise Exception(
                f"Story with id {self.story_id} not found or already updated"
            )

        return "Story updated successfully"       
    