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