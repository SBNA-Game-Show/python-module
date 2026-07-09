import os
from uuid import uuid4

from utils.file_system_reader import FileSystemReader
from services.clean_tokenized_english_words_array import CleanEnglishTokenizedData
from services.extract_definitions_english_words import ExtractDefinitions
from services.extract_english_synonym_antonym import ExtractEnglishSynonymAntonym
from services.tokenize_english_passage import TokenizeEnglishVersion
from services.tokenize_sanskrit_passage_web import TokenizeSanskritPassageWeb
from repository.learnsanskrit_metadata_repo import WriteTokenizedStoryToMongoDB


class ReadUploadedJSON:
    def __init__(self, fileName):
        if not fileName:
            raise ValueError("File name not provided.")

        self.fileName = fileName

        _, extension = os.path.splitext(fileName)

        if extension.lower() != ".json":
            raise RuntimeError(
                f"Incorrect file type '{extension}'. Expected a JSON file."
            )

        self.tokenized_data = []

    def execute(self):

        raw_data = self._read_file(self.fileName)

        # ---------------------------
        # Single passage JSON
        # ---------------------------
        if isinstance(raw_data, dict):

            normalized_data = self._normalize_passage(raw_data)
            final_data = self._tokenize_passage(normalized_data)

            return self._write_to_DB(final_data)

        # ---------------------------
        # Multiple passage JSON
        # ---------------------------
        elif isinstance(raw_data, list):

            for item in raw_data:
                normalized_data = self._normalize_passage(item)
                tokenized = self._tokenize_passage(normalized_data)
                self.tokenized_data.append(tokenized)

            if not self.tokenized_data:
                raise RuntimeError(
                    "Tokenized data is empty after processing multi-passage JSON."
                )

            results = []

            for passage in self.tokenized_data:
                results.append(self._write_to_DB(passage))

            return results

        else:
            raise RuntimeError("Uploaded JSON must contain either an object or a list.")

    def _read_file(self, fileName):
        reader = FileSystemReader(fileName)
        return reader.read_file()

    def _normalize_passage(self, data):
        return {
            "_id": str(uuid4()),
            "title": {
                "englishVersion": data["englishTitle"],
                "sanskritVersion": data["sanskritTitle"],
            },
            "englishVersion": data["englishPassage"],
            "sanskritVersion": data["sanskritPassage"],
        }

    def _tokenize_passage(self, passage):

        eng_tokenizer = TokenizeEnglishVersion(passage)
        eng_tokenized = eng_tokenizer.tokenize_english_version()

        eng_synonymize = ExtractEnglishSynonymAntonym(eng_tokenized)
        eng_synonym_added = eng_synonymize.execute()

        definition_adder = ExtractDefinitions(eng_synonym_added)
        definition_added = definition_adder.execute()

        eng_cleaner = CleanEnglishTokenizedData(definition_added)
        cleaned_data = eng_cleaner.execute()

        sa_tokenizer = TokenizeSanskritPassageWeb(cleaned_data)
        final_data = sa_tokenizer.tokenize()

        return final_data

    def _write_to_DB(self, data):
        writer = WriteTokenizedStoryToMongoDB(data)
        return writer.save_story()