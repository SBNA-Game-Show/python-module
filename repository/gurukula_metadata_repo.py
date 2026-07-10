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

        document = {
            "createdAt": datetime.utcnow(),
            "categories": self.data
        }

        return document