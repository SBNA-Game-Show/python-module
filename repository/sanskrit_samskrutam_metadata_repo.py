from config.dbconfig import connect_db
from datetime import datetime


class WriteMetaData:

    def __init__(self, data):
        self.db = connect_db()
        self.collection = self.db["samskrutam_metadata"]
        self.data = data

    def write(self):

        if not isinstance(self.data, list):
            self.data = [self.data]

        for doc in self.data:

            if "createdAt" not in doc:
                doc["createdAt"] = datetime.utcnow()

            self.collection.update_one(
                {"source": doc["source"]},
                {"$set": doc},
                upsert=True
            )

        return len(self.data)
    
    
class GetUnusedStories:

    def __init__(self):
        self.db = connect_db()
        self.collection = self.db["samskrutam_metadata"]

    def execute(self) -> list:
        """Retrieves all stories across all sources where used is false.

        Returns:
            list: A list of dictionaries containing all unused stories.
        """
        pipeline = [
            # 1. Flatten the stories array from all documents
            {"$unwind": "$stories"},
            # 2. Filter for only the stories where used is False
            {"$match": {"stories.used": False}},
            # 3. Reshape the output to easily consume the story objects
            {
                "$project": {
                    "_id": "$stories._id",
                    "vendorId": "$stories.vendorId",
                    "sanskrit_title": "$stories.sanskrit_title",
                    "english_title": "$stories.english_title",
                    "used": "$stories.used",
                    "source": "$source",  # Tracks which source page it came from
                }
            },
        ]

        # Execute and return the list of unused stories
        return list(self.collection.aggregate(pipeline))
        

        