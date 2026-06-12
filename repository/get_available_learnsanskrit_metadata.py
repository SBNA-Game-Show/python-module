from config.dbconfig import connect_db

class GetUnusedStories:

    def __init__(self):
        self.db = connect_db()
        self.collection = self.db["learnsank_meta"]

    def get_all(self):
        # 1. Fetch entire documents that contain at least one 'used: False' story
        cursor = self.collection.find({"story_description.used": False})
        
        filtered_documents = []

        for document in cursor:
            # 2. Extract the story list safely
            all_stories = document.get("story_description", [])
            
            # 3. Keep only the stories where 'used' is strictly False
            unused_stories = [story for story in all_stories if story.get("used") is False]
            
            # 4. Replace the old array inside the document with the filtered list
            document["story_description"] = unused_stories
            
            # 5. Add the complete, cleaned document to your results
            filtered_documents.append(document)
                    
        return filtered_documents