import pytest
from unittest.mock import patch

from services.extract_english_synonym_antonym import (
    ExtractEnglishSynonymAntonym
)


class TestExtractEnglishSynonymAntonym:

    @pytest.fixture
    def sample_data(self):
        return {
            "tokenized_english_version": [
                {
                    "text": "good",
                    "lemma": "good",
                    "pos": "ADJ"
                },
                {
                    "text": "run",
                    "lemma": "run",
                    "pos": "VERB"
                }
            ]
        }

    def test_extract_data(self):

        extractor = ExtractEnglishSynonymAntonym({
            "tokenized_english_version": [
                {"word": "test"}
            ]
        })

        result = extractor._extract_data(
            extractor.data
        )

        assert result == [
            {"word": "test"}
        ]

    def test_extract_data_missing_key(self):

        extractor = ExtractEnglishSynonymAntonym({})

        result = extractor._extract_data(
            extractor.data
        )

        assert result == []

    @patch(
        "services.extract_english_synonym_antonym.GetSynonyms"
    )
    @patch(
        "services.extract_english_synonym_antonym.GetAntonyms"
    )
    def test_execute(
        self,
        mock_antonyms_class,
        mock_synonyms_class,
        sample_data
    ):

        mock_synonyms_class.return_value.execute.return_value = [
            "excellent",
            "great"
        ]

        mock_antonyms_class.return_value.execute.return_value = [
            "bad"
        ]

        extractor = ExtractEnglishSynonymAntonym(
            sample_data
        )

        result = extractor.execute()

        assert "tokenized_english_version" in result

        token = result[
            "tokenized_english_version"
        ][0]

        assert token["synonyms"] == [
            "excellent",
            "great"
        ]

        assert token["antonyms"] == [
            "bad"
        ]

    @patch(
        "services.extract_english_synonym_antonym.GetSynonyms"
    )
    @patch(
        "services.extract_english_synonym_antonym.GetAntonyms"
    )
    def test_execute_multiple_tokens(
        self,
        mock_antonyms_class,
        mock_synonyms_class,
        sample_data
    ):

        mock_synonyms_class.return_value.execute.return_value = [
            "synonym"
        ]

        mock_antonyms_class.return_value.execute.return_value = [
            "antonym"
        ]

        extractor = ExtractEnglishSynonymAntonym(
            sample_data
        )

        result = extractor.execute()

        assert len(
            result["tokenized_english_version"]
        ) == 2

        for token in result[
            "tokenized_english_version"
        ]:
            assert token["synonyms"] == [
                "synonym"
            ]

            assert token["antonyms"] == [
                "antonym"
            ]

    @patch(
        "services.extract_english_synonym_antonym.GetSynonyms"
    )
    @patch(
        "services.extract_english_synonym_antonym.GetAntonyms"
    )
    def test_execute_empty_tokens(
        self,
        mock_antonyms_class,
        mock_synonyms_class
    ):

        extractor = ExtractEnglishSynonymAntonym({
            "tokenized_english_version": []
        })

        result = extractor.execute()

        assert result[
            "tokenized_english_version"
        ] == []

        mock_synonyms_class.assert_not_called()
        mock_antonyms_class.assert_not_called()