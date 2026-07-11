from config.dbconfig import connect_db


class BaseRepository:

    collection_name = None

    def __init__(self):

        self.db = connect_db()

        if not self.collection_name:
            raise ValueError(
                "collection_name is not defined"
            )

        self.collection = self.db[self.collection_name]