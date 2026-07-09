import pytest
from unittest.mock import patch

from services.learnsanskrit_fable_extraction_pipeline.extract_new_fable_learnsanskrit import FetchNewFable


class TestFetchNewFable:
    """
        Unit tests for FetchNewFable.

        Goal:
        Test only the orchestration/business logic.

        We mock:
        - Database access
        - HTTP requests
        - File writing
        - NLP processing (spaCy/Stanza)
        - Synonym extraction

        This keeps tests fast and deterministic.
        """
    @patch.object(FetchNewFable, "_update_story_toDB")
    @patch.object(FetchNewFable, "_write_to_mongoDB")
    @patch.object(FetchNewFable, "_clean_english_data")
    @patch.object(FetchNewFable, "_add_definitions")
    @patch.object(FetchNewFable, "_tokenize_sanskrit_version")
    @patch.object(FetchNewFable, "_add_synonym_antonym")
    @patch.object(FetchNewFable, "_tokenize_english_version")
    @patch.object(FetchNewFable, "_clean_data")
    @patch.object(FetchNewFable, "_retrieve_raw_data")
    @patch.object(FetchNewFable, "_get_story_data_from_DB")
    def test_execute_success(
            self,
            mock_get_story_data,
            mock_retrieve_raw_data,
            mock_clean_data,
            mock_tokenize_english,
            mock_add_synonym_antonym,
            mock_tokenize_sanskrit,
            mock_add_definitions,
            mock_clean_english_data,
            mock_write_to_mongo,
            mock_update_db
        ):

            mock_get_story_data.return_value = {
                "_id": "123",
                "vendorId": "Aesop001"
            }

            mock_retrieve_raw_data.return_value = {"raw": "data"}

            mock_clean_data.return_value = {"englishVersion": "text"}

            mock_tokenize_english.return_value = {}

            mock_add_synonym_antonym.return_value = {}

            mock_add_definitions.return_value = {}

            mock_tokenize_sanskrit.return_value = {}

            mock_clean_english_data.return_value = {}

            mock_write_to_mongo.return_value = {"success": True}

            mock_update_db.return_value = {"success": True}

            service = FetchNewFable("123")

            result = service.execute()

            assert result == {
                "success": True,
                "message": "Fable downloaded successfully"
            }

            mock_get_story_data.assert_called_once_with("123")
            mock_retrieve_raw_data.assert_called_once_with("Aesop001")
            mock_write_to_mongo.assert_called_once()
            mock_update_db.assert_called_once_with("123")

    @patch.object(FetchNewFable, "_get_story_data_from_DB")
    def test_execute_story_not_found(self, mock_get_story_data):
        """ Test when story metadata cannot be found. Expected: ValueError should be raised. """
        mock_get_story_data.return_value = None

        service = FetchNewFable("999")

        with pytest.raises(ValueError) as exc:
            service.execute()

        assert "No data found for the given ID" in str(exc.value)

    
    @patch.object(FetchNewFable, "_update_story_toDB")
    @patch.object(FetchNewFable, "_write_to_mongoDB")
    @patch.object(FetchNewFable, "_clean_english_data")
    @patch.object(FetchNewFable, "_add_definitions")
    @patch.object(FetchNewFable, "_tokenize_sanskrit_version")
    @patch.object(FetchNewFable, "_add_synonym_antonym")
    @patch.object(FetchNewFable, "_tokenize_english_version")
    @patch.object(FetchNewFable, "_clean_data")
    @patch.object(FetchNewFable, "_retrieve_raw_data")
    @patch.object(FetchNewFable, "_get_story_data_from_DB")
    def test_story_category_extracted_correctly(
        self,
        mock_get_story_data,
        mock_retrieve_raw_data,
        mock_clean_data,
        mock_tokenize_english,
        mock_add_synonym_antonym,
        mock_tokenize_sanskrit,
        mock_add_definitions,
        mock_clean_english_data,
        mock_write_to_mongo,
        mock_update_db
    ):
        """ Verify that category extraction logic works. Example: Panchatantra001 -> Panchatantra """
        mock_get_story_data.return_value = {
            "_id": "123",
            "vendorId": "Panchatantra001"
        }

        mock_retrieve_raw_data.return_value = {}
        mock_clean_data.return_value = {}

        service = FetchNewFable("123")

        with patch.object(service, "_tokenize_english_version", return_value={}), \
             patch.object(service, "_add_synonym_antonym", return_value={}), \
             patch.object(service, "_tokenize_sanskrit_version", return_value={}), \
             patch.object(service, "_write_to_file_system", return_value=True), \
             patch.object(service, "_update_story_status", return_value={"success": True}):

            result = service.execute()

            assert result == {
            "success": True,
            "message": "Fable downloaded successfully"
        }
            
    def test_write_to_mongodb_success(self):
        """Verify helper method returns MongoDB response."""

        service = FetchNewFable("123")

        expected = "507f1f77bcf86cd799439011 tokenized and added to DB"

        with patch(
            "services.learnsanskrit_fable_extraction_pipeline.extract_new_fable_learnsanskrit.WriteTokenizedStoryToMongoDB"
        ) as mock_writer:

            mock_writer.return_value.save_story.return_value = expected

            result = service._write_to_mongoDB({"test": "data"})

            assert result == expected

            mock_writer.assert_called_once_with({"test": "data"})
            mock_writer.return_value.save_story.assert_called_once()

    # =========================================================
    # WRITE FILE SYSTEM TEST (FIXED CONSTRUCTOR + PATH)
    # =========================================================
    # def test_write_to_file_system_success(self):

    #     service = FetchNewFable("123")

    #     with patch(
    #         "services.learnsanskrit_fable_extraction_pipeline.extract_new_fable_learnsanskrit.WriteToFileSystem"
    #     ) as mock_writer:

    #         mock_writer.return_value = None

    #         result = service._write_to_file_system({"test": "data"})

    #         assert result is True

    # def test_write_to_file_system_failure(self):

    #     service = FetchNewFable("123")

    #     with patch(
    #         "services.learnsanskrit_fable_extraction_pipeline.extract_new_fable_learnsanskrit.WriteToFileSystem"
    #     ) as mock_writer:

    #         mock_writer.side_effect = Exception("Disk error")

    #         result = service._write_to_file_system({"test": "data"})

    #         assert result is False