from utils.tokenized_story_mapper import TokenizedStoryMapper
from repository.base_repository import BaseRepository


class GetTokenizedStoryByIdFromMongoDB(BaseRepository):
    
    collection_name = "tokenized_stories"

    def __init__(self, story_id):
        super().__init__()

        self.story_id = story_id

    def get_story(self):
        data = self.collection.find_one({"_id": self.story_id})

        if data is None:
            return {
                "success": False,
                "message": "No tokenized story found for the given ID."
            }

        return data
    
    
class GetAllTokenizedStoriesFromMongoDB(BaseRepository):
    
    collection_name = "tokenized_stories"
    def __init__(self):
        super().__init__()

        
        
    def get_all(self):
        stories = list(self.collection.find())


        return {
            "success": True,
            "count": len(stories),
            "data": stories
        }
        
        
class GetTokenizedStoriesByCategoryFromMongoDB(BaseRepository):
    
    collection_name = "tokenized_stories"

    def __init__(self, category_name):
        super().__init__()
        
        self.category = category_name

    def get_stories(self):
        data = list(
            self.collection.find({"category": self.category})
        )

        if not data:
            return {
                "success": False,
                "message": f"No tokenized stories found for category '{self.category}'."
            }

        return {
            "success": True,
            "count": len(data),
            "data": data
        }
        
class EditTokenizedStory(BaseRepository):
    collection_name = "tokenized_stories"
    def __init__(self, storyId, data):
        super().__init__()
        
        if not storyId:
            raise ValueError("Story Id is Required")
        if not data:
            raise ValueError("Tokenized Story not provided")

        self.storyId = storyId
        self.data = data
        
        
    def update(self):
        
        story = self.collection.find_one({"_id": self.storyId})
        
        if not story:
            return ValueError("No Story Found By Given Id")
        
        doc = TokenizedStoryMapper.to_schema(self.data)
        
        result = self.collection.update_one(
            {"_id": self.storyId},{"$set":doc}
            )
        
        if result.modified_count == 0:
            return {
                "success":False,
                "message":"No Changes where Made"
            }
            
        return {
            "success":True,
            "message": "Tokenized Story Updated SuccessFully"
        }

        