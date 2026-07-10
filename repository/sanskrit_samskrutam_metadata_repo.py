from datetime import datetime

from repository.base_repository import BaseRepository


class WriteMetaData(BaseRepository):
    collection_name = "samskrutam_metadata"
    
    def __init__(self, data):
        super().__init__()

        self.data = data

    def write(self):

        if not isinstance(self.data, list):
            self.data = [self.data]

        for doc in self.data:

            if "createdAt" not in doc:
                doc["createdAt"] = datetime.utcnow()

            self.collection.update_one(
                {"source": doc["source"]},
                {"$set": doc},
                upsert=True
            )

        return len(self.data)
    
    
class GetUnusedStories(BaseRepository):
    
    collection_name = "samskrutam_metadata"

    def __init__(self):
        super().__init__()

    def get_all(self) -> list:
        """Retrieves all stories across all sources where used is false.

        Returns:
            list: A list of dictionaries containing all unused stories.
        """
        pipeline = [
            # 1. Flatten the stories array from all documents
            {"$unwind": "$stories"},
            # 2. Filter for only the stories where used is False
            {"$match": {"stories.used": False}},
            # 3. Reshape the output to easily consume the story objects
            {
                "$project": {
                    "_id": "$stories._id",
                    "vendorId": "$stories.vendorId",
                    "sanskrit_title": "$stories.sanskrit_title",
                    "english_title": "$stories.english_title",
                    "used": "$stories.used",
                    "source": "$source",  # Tracks which source page it came from
                }
            },
        ]

        # Execute and return the list of unused stories
        return list(self.collection.aggregate(pipeline))
    
class GetStoryDataById(BaseRepository):
    
    collection_name = "samskrutam_metadata"

    def __init__(self, storyId):
        super().__init__()
        
        self.storyId = storyId

    def get_data(self) -> dict or None: # type: ignore
        """Retrieves parent metadata (url, source) and the specific story details

        matching the given storyId.
        """
        # 1. Target the exact document containing the story ID
        query = {"stories._id": self.storyId}

        # 2. Project the parent fields and isolate ONLY the matching story element
        projection = {
            "source": 1,
            "source_url": 1,
            "stories": {"$elemMatch": {"_id": self.storyId}},
        }

        # 3. Execute find_one using standard Mongo syntax
        doc = self.collection.find_one(query, projection)

        if not doc or "stories" not in doc:
            return None

        # 4. Extract the isolated story from the array
        story_details = doc["stories"][0]

        # 5. Package everything together nicely
        return {
            "source": doc.get("source"),
            "source_url": doc.get("source_url"),
            "story_id": story_details.get("_id"),
            "vendorId": story_details.get("vendorId"),
            "sanskrit_title": story_details.get("sanskrit_title"),
            "english_title": story_details.get("english_title"),
            "used": story_details.get("used"),
        }
        
class UpdateStoryToUsed (BaseRepository):
    
    collection_name = "samskrutam_metadata"

    def __init__(self, storyId):
        super().__init__()
        self.storyId = storyId

    def update(self) -> bool:
        """Finds the story by its ID inside the array and updates its 'used' field

        to True. Returns True if modified, False otherwise.
        """
        # 1. Target the document AND the specific item inside the array
        query = {"stories._id": self.storyId}

        # 2. Use the positional operator ($) to update the matched array element
        update_op = {"$set": {"stories.$.used": True}}

        # 3. Execute the update match
        result = self.collection.update_one(query, update_op)

        # Returns True if a document was found and updated
        return result.modified_count > 0
    

    
    
        

        