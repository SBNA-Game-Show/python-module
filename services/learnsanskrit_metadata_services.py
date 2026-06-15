from repository.learnsanskrit_metadata_repo import GetUnusedStories

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