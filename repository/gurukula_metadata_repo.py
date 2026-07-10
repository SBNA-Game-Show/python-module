from config.dbconfig import connect_db
from datetime import datetime


class WriteMetaData:

    def __init__(self, data):
        self.data = data
        self.db = connect_db()
        self.collection = self.db["gurukula_metadata"]


    def write(self):

        document = self._prepare_document()

        result = self.collection.insert_one(document)

        return {
            "inserted_id": str(result.inserted_id)
        }


    def _prepare_document(self):

        return {
            "createdAt": datetime.utcnow(),
            "categories": self.data["categories"]
        }
    
class RetrieveUnusedStories:

    def __init__(self):
        self.db = connect_db()
        self.collection = self.db["gurukula_metadata"]


    def get_all(self):

        pipeline = [
            {
                "$project": {
                    "categories": {
                        "$objectToArray": "$categories"
                    }
                }
            },
            {
                "$unwind": "$categories"
            },
            {
                "$unwind": "$categories.v.stories"
            },
            {
                "$match": {
                    "categories.v.stories.used": False
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "category": "$categories.k",
                    "category_link": "$categories.v.category_link",
                    "story": "$categories.v.stories"
                }
            }
        ]

        return list(self.collection.aggregate(pipeline))
    