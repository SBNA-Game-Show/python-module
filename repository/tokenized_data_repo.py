from config.dbconfig import connect_db


class GetTokenizedStoryByIdFromMongoDB:

    def __init__(self, story_id):
        self.db = connect_db()
        self.collection = self.db["tokenized_stories"]
        self.story_id = story_id

    def get_story(self):
        data = self.collection.find_one({"_id": self.story_id})

        if data is None:
            return {
                "success": False,
                "message": "No tokenized story found for the given ID."
            }

        return data
    
    
class GetAllTokenizedStoriesFromMongoDB:
    def __init__(self):
        self.db = connect_db()
        self.collection = self.db["tokenized_stories"]
        
        
    def get_all(self):
        stories = list(self.collection.find())


        return {
            "success": True,
            "count": len(stories),
            "data": stories
        }
        
        
class GetTokenizedStoriesByCategoryFromMongoDB:

    def __init__(self, category_name):
        self.db = connect_db()
        self.collection = self.db["tokenized_stories"]
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