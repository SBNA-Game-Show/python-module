from config.dbconfig import connect_db

class GetMetaDataById:

    def __init__(self, story_id):
        self.story_id = story_id
        self.db = connect_db()
        self.collection = self.db["learnsank_meta"]
        
    def get_data(self):
        # 1. Use .find() instead of .findall() to get all documents
        docs = self.collection.find()
        
        # 2. Iterate through the documents (categories)
        for category in docs:
            stories = category.get("story_description", [])
            
            # 3. Iterate through the nested stories array
            for story in stories:
                # Fixed: Added quotes around "_id"
                if story.get("_id") == self.story_id:
                    
                    # Return the matched story object along with parent meta if desired
                    return story
        return None