from repository.gurukula_metadata_repo import RetrieveUnusedStories


def retrieve_all():
        try:
           
            req = RetrieveUnusedStories()
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
    