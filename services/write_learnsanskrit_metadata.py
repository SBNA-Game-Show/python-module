from repository.write_learnsanskrit_meta_data_to_mongodb import WriteLearnSanskritMetaData


class WriteLearnSanskritCCMetaData:

    def execute(self):
        try:
            req = WriteLearnSanskritMetaData()
            return req.execute()

        except Exception as e:
            raise Exception(f"Failed to write LearnSanskrit metadata: {str(e)}")