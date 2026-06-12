from repository.file_system.get_all_story_data_learnsanskrit import GetAllStoryDataLearnSanskrit
from repository.get_available_learnsanskrit_metadata import GetUnusedStories

class RetrieveAllStoryDataLearnSanskrit:
    
    def retrieve_all(self):
        try:
            # # From File System
            # data =  GetAllStoryDataLearnSanskrit().get_all_story_data()
            
            req = GetUnusedStories()
            data = req.get_all()
            
            return{
                "success":True,
                "data":data
            }
            
        except Exception as e:
            return{
                "success":False,
                "message":str(e)
            }