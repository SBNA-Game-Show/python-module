from datetime import datetime
from repository.base_repository import BaseRepository


class WriteMetaData(BaseRepository):
    collection_name = "gurukula_metadata"

    def __init__(self, data):
        super().__init__()
        
        self.data = data

    def write(self):

        document = self._prepare_document()

        result = self.collection.insert_one(document)

        return {
            "inserted_id": str(result.inserted_id)
        }


    def _prepare_document(self):

        return {
            "createdAt": datetime.utcnow(),
            "categories": self.data["categories"]
        }
    
class RetrieveUnusedStories(BaseRepository):
    collection_name = "gurukula_metadata"

    def __init__(self):
        super().__init__()


    def get_all(self):

        pipeline = [
            {
                "$project": {
                    "categories": {
                        "$objectToArray": "$categories"
                    }
                }
            },
            {
                "$unwind": "$categories"
            },
            {
                "$unwind": "$categories.v.stories"
            },
            {
                "$match": {
                    "categories.v.stories.used": False
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "category": "$categories.k",
                    "category_link": "$categories.v.category_link",
                    "story": "$categories.v.stories"
                }
            }
        ]

        return list(self.collection.aggregate(pipeline))
    
class RetrieveStoryById(BaseRepository):
    collection_name = "gurukula_metadata"

    def __init__(self, storyId):
        super().__init__()
        if not storyId:
            raise ValueError("Story Id is Required")

        self.storyId = storyId


    def get(self):

        pipeline = [
            {
                "$project": {
                    "categories": {
                        "$objectToArray": "$categories"
                    }
                }
            },
            {
                "$unwind": "$categories"
            },
            {
                "$unwind": "$categories.v.stories"
            },
            {
                "$match": {
                    "categories.v.stories._id": self.storyId
                }
            },
            {
                "$replaceWith": "$categories.v.stories"
            }
        ]

        result = list(self.collection.aggregate(pipeline))

        return result[0] if result else None
    
    
        

    