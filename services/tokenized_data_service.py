
from repository.tokenized_data_repo import GetTokenizedStoryByIdFromMongoDB,GetAllTokenizedStoriesFromMongoDB,GetTokenizedStoriesByCategoryFromMongoDB,EditTokenizedStory


class RetrieveTokenizedStoryById:

    def __init__(self, story_id):

        if story_id is None:
            raise ValueError("story_id cannot be None")

        self.story_id = story_id

    def retrieve_story(self):
        
        
        repo = GetTokenizedStoryByIdFromMongoDB(self.story_id)
        story = repo.get_story()

        if story is None:
            raise LookupError("Story not found")

        return story
    
class RetrieveTokenizedStories:

    def get_all(self):
        try:
            
            # Query database
            repo = GetAllTokenizedStoriesFromMongoDB()
            data = repo.get_all()

            return data

        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }
            
            
class RetrieveTokenizedStoryByCategory:
    
    def __init__(self, category_name):       
        
        self.category = category_name        
        
    
    def get_by_category(self):
        try:
            
            # # From Databases
            repo = GetTokenizedStoriesByCategoryFromMongoDB(self.category)
            data = repo.get_stories()
            
            return data
            
        except Exception as e:
            return{
                "success":False,
                "message":str(e)
                
            }
            

class UpdateTokenizedStory:
    def __init__(self,storyId,tokenizedData):
        if not storyId:
            raise ValueError("Story Id is Required")
        if not tokenizedData:
            raise ValueError("Tokenized Story not provided")
        self.storyId = storyId
        self.tokenizedData = tokenizedData
        
    def update_tokenized(self):
        
        try:
            updater = EditTokenizedStory(self.storyId,self.tokenizedData)
            result = updater.update()
            
            return result
            
        except Exception as e:
            return{
                "success":False,
                "message":str(e)
            }
    
    
    