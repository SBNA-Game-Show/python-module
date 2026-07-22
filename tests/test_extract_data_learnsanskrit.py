import json
import pytest

from services.learnsanskrit_fable_extraction_pipeline.convert_to_JSON import (
    ExtractDataFromLearnSanskrit,
)


class TestExtractDataFromLearnSanskrit:
    """Tests data extraction and transformation from LearnSanskrit API responses."""

    @pytest.fixture
    def sample_data(self):
        """Sample LearnSanskrit API response."""
        return {
            "data": {
                "summary_head": [
                    "Lion, Mouse",
                    "Kindness is rewarded"
                ],
                "summary_text": "A lion once spared a mouse.",
                "texts": [
                    "<div>siṃhaḥ</div><div>mūṣakaḥ</div>"
                ],
                "textsdeva": [
                    "<div>सिंहः</div><div>मूषकः</div>"
                ]
            }
        }

    def test_parse_json_dictionary(self, sample_data):
        extractor = ExtractDataFromLearnSanskrit(sample_data)

        assert extractor.data == sample_data

    def test_parse_json_string(self, sample_data):
        json_string = json.dumps(sample_data)

        extractor = ExtractDataFromLearnSanskrit(json_string)

        assert extractor.data == sample_data

    def test_parse_json_invalid_data(self):
        with pytest.raises(ValueError) as exc:
            ExtractDataFromLearnSanskrit("INVALID_JSON")

        assert str(exc.value) == "INVALID JSON DATA"

    def test_init_with_empty_data(self):
        with pytest.raises(ValueError) as exc:
            ExtractDataFromLearnSanskrit(None)

        assert str(exc.value) == "DATA IS NOT PROVIDED TO CONVERT TO JSON"

    def test_extract_english_title(self, sample_data):
        extractor = ExtractDataFromLearnSanskrit(sample_data)

        assert extractor._extract_english_title() == "Lion, Mouse"

    def test_extract_actors(self, sample_data):
        extractor = ExtractDataFromLearnSanskrit(sample_data)

        assert extractor._extract_actors() == [
            "Lion",
            "Mouse",
        ]

    def test_extract_moral(self, sample_data):
        extractor = ExtractDataFromLearnSanskrit(sample_data)

        assert extractor._extract_moral() == "Kindness is rewarded"

    def test_extract_moral_removes_parentheses(self):
        data = {
            "data": {
                "summary_head": [
                    "Lion",
                    "(Be Kind)"
                ],
                "summary_text": "Story",
                "textsdeva": [
                    "<div>शब्द</div>"
                ]
            }
        }

        extractor = ExtractDataFromLearnSanskrit(data)

        assert extractor._extract_moral() == "Be Kind"

    def test_extract_english_story(self, sample_data):
        extractor = ExtractDataFromLearnSanskrit(sample_data)

        assert extractor._extract_english_version_story() == (
            "A lion once spared a mouse."
        )

    def test_extract_sanskrit_version(self, sample_data):
        extractor = ExtractDataFromLearnSanskrit(sample_data)

        assert extractor._extract_sanskrit_version_story() == [
            "सिंहः मूषकः"
        ]

    def test_extract_sanskrit_title(self, sample_data):
        extractor = ExtractDataFromLearnSanskrit(sample_data)

        assert (
            extractor._extracting_sanskrit_version_story_title()
            == "सिंहः मूषकः"
        )

    def test_get_json_data(self, sample_data):
        extractor = ExtractDataFromLearnSanskrit(sample_data)

        result = extractor.get_json_data()

        assert result == {
            "title": {
                "englishVersion": "Lion, Mouse",
                "sanskritVersion": "सिंहः मूषकः",
            },
            "actors": [
                "Lion",
                "Mouse",
            ],
            "storyMoral": [
                "Kindness is rewarded",
            ],
            "englishVersion": "A lion once spared a mouse.",
            "sanskritVersion": [
                "सिंहः मूषकः",
            ],
        }

    def test_empty_sanskrit_sections(self):
        data = {
            "data": {
                "summary_head": [
                    "Lion",
                    "Moral",
                ],
                "summary_text": "Story",
                "textsdeva": [
                    "<div></div><div>123</div><div>शब्द</div>"
                ],
            }
        }

        extractor = ExtractDataFromLearnSanskrit(data)

        assert extractor._extract_sanskrit_version_story() == [
            "शब्द"
        ]

    def test_multiple_sanskrit_sections(self):
        data = {
            "data": {
                "summary_head": [
                    "Lion",
                    "Moral",
                ],
                "summary_text": "Story",
                "textsdeva": [
                    "<div>शब्द१</div><div>शब्द२</div>",
                    "<div>शब्द३</div><div>शब्द४</div>",
                ],
            }
        }

        extractor = ExtractDataFromLearnSanskrit(data)

        assert extractor._extract_sanskrit_version_story() == [
            "शब्द१ शब्द२",
            "शब्द३ शब्द४",
        ]

    def test_ignore_numeric_only_sections(self):
        data = {
            "data": {
                "summary_head": [
                    "Lion",
                    "Moral",
                ],
                "summary_text": "Story",
                "textsdeva": [
                    "<div>1</div><div>2</div><div>3</div>"
                ],
            }
        }

        extractor = ExtractDataFromLearnSanskrit(data)

        assert extractor._extract_sanskrit_version_story() == []

    def test_parse_json_list(self):
        data = [{"name": "story"}]

        extractor = ExtractDataFromLearnSanskrit(data)

        assert extractor.data == data