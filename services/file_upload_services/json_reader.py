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


        # Single passage JSON
        if isinstance(raw_data, dict):

            normalized_data = self._normalize_passage(raw_data)
            final_data = self._tokenize_passage(normalized_data)

            result = self._write_to_DB(final_data)

            if result.endswith("added to DB"):
                self._delete_file()

            return result


        # Multiple passage JSON
        elif isinstance(raw_data, list):

            results_array = []

            for item in raw_data:

                normalized_data = self._normalize_passage(item)

                tokenized = self._tokenize_passage(
                    normalized_data
                )

                self.tokenized_data.append(tokenized)


            for passage in self.tokenized_data:

                result = self._write_to_DB(passage)

                results_array.append(result)


            # Check after processing all stories
            if all(
                result.endswith("added to DB")
                for result in results_array
            ):

                self._delete_file()

                return {
                    "success": True,
                    "message": (
                        f"{len(results_array)} stories "
                        "Tokenized and Added to DB"
                    )
                }


            return {
                "success": False,
                "message": "Some stories failed to write to DB",
                "results": results_array
            }


        else:
            raise RuntimeError(
                "Uploaded JSON must contain either an object or a list."
            )


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

        eng_tokenized = (
            eng_tokenizer.tokenize_english_version()
        )


        eng_synonymize = ExtractEnglishSynonymAntonym(
            eng_tokenized
        )

        eng_synonym_added = (
            eng_synonymize.execute()
        )


        definition_adder = ExtractDefinitions(
            eng_synonym_added
        )

        definition_added = (
            definition_adder.execute()
        )


        eng_cleaner = CleanEnglishTokenizedData(
            definition_added
        )

        cleaned_data = (
            eng_cleaner.execute()
        )


        sa_tokenizer = TokenizeSanskritPassageWeb(
            cleaned_data
        )

        return sa_tokenizer.tokenize()



    def _write_to_DB(self, data):

        writer = WriteTokenizedStoryToMongoDB(data)

        return writer.save_story()



    def _delete_file(self):

        reader = FileSystemReader(self.fileName)

        file_path = reader.file_path

        if os.path.exists(file_path):
            os.remove(file_path)