
from repository.file_system.get_tokenized_story_by_Id import GetTokenizedStoryById
from repository.tokenized_data_repo import GetTokenizedStoryByIdFromMongoDB,GetAllTokenizedStoriesFromMongoDB,GetTokenizedStoriesByCategoryFromMongoDB


class RetrieveTokenizedStoryById:

    def __init__(self, story_id):

        if story_id is None:
            raise ValueError("story_id cannot be None")

        self.story_id = story_id

    def retrieve_story(self):
        
        # # Retrieves from file system
        # repository = GetTokenizedStoryById(self.story_id)

        # story = repository.retrieve_story()
        
        # Retrieving from Database
        
        repo = GetTokenizedStoryByIdFromMongoDB(self.story_id)
        story = repo.get_story()

        if story is None:
            raise LookupError("Story not found")

        return story
    
class RetrieveTokenizedStories:

    def get_all(self):
        try:
            # #using file system to write data
            # data = GetAllTokenizedStories().get_all_stories()
            
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
            # # reading from file system
            # repo = GetTokenizedStoryByCategory(self.category)
            # data = repo.retrieve_story()
            
            # # From Databases
            repo = GetTokenizedStoriesByCategoryFromMongoDB(self.category)
            data = repo.get_stories()
            
            return data
            
        except Exception as e:
            return{
                "success":False,
                "message":str(e)
                
            }