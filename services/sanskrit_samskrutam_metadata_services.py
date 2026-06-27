from repository.sanskrit_samskrutam_metadata_repo import GetUnusedStories

def retrieve_all():
    
        try:
           
            req = GetUnusedStories()
            data = req.execute()
            
            return{
                "success":True,
                "data":data
            }
            
        except Exception as e:
            return{
                "success":False,
                "message":str(e)
            }
    