from services.learnsanskrit_metadata_extraction_pipeline.extract_data import RetrieveMetaData

from repository.learnsanskrit_metadata_repo import LearnSanskritMetaDataRepository

from utils.learnsanskrit_metadata_mapper import (
    LearnSanskritMetaDataMapper
)


class WriteLearnSanskritCCMetaData:

    def __init__(self):

        self.extractor = (
            RetrieveMetaData()
        )

        self.repository = (
            LearnSanskritMetaDataRepository()
        )

    def execute(self):

        data = (
            self.extractor.execute()
        )

        docs = [
            LearnSanskritMetaDataMapper.to_schema(
                item
            )
            for item in data
        ]

        result = (
            self.repository.save_many(
                docs
            )
        )

        return {
            "inserted_count":
                len(result.inserted_ids)
        }