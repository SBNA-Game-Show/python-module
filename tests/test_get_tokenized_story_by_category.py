from unittest.mock import MagicMock

from repository.tokenized_data_repo import (
    GetTokenizedStoriesByCategoryFromMongoDB
)


class TestGetTokenizedStoriesByCategoryFromMongoDB:


    def test_get_stories_by_category_success(self):

        repo = GetTokenizedStoriesByCategoryFromMongoDB(
            "Panchatantra"
        )

        repo.collection = MagicMock()

        repo.collection.find.return_value = [
            {
                "_id": "1",
                "title": "Rabbit Story",
                "category": "Panchatantra"
            },
            {
                "_id": "2",
                "title": "Lion Story",
                "category": "Panchatantra"
            }
        ]


        result = repo.get_stories()


        assert result["success"] is True

        assert result["count"] == 2

        assert len(result["data"]) == 2

        assert result["data"][0]["title"] == (
            "Rabbit Story"
        )

        assert result["data"][1]["title"] == (
            "Lion Story"
        )


        repo.collection.find.assert_called_once_with(
            {
                "category": "Panchatantra"
            }
        )



    def test_get_stories_by_category_single_result(self):

        repo = GetTokenizedStoriesByCategoryFromMongoDB(
            "Aesop"
        )

        repo.collection = MagicMock()

        repo.collection.find.return_value = [
            {
                "_id": "10",
                "title": "Fox Story",
                "category": "Aesop"
            }
        ]


        result = repo.get_stories()


        assert result["success"] is True

        assert result["count"] == 1

        assert result["data"][0]["category"] == (
            "Aesop"
        )



    def test_get_stories_by_category_not_found(self):

        repo = GetTokenizedStoriesByCategoryFromMongoDB(
            "Unknown"
        )

        repo.collection = MagicMock()

        repo.collection.find.return_value = []


        result = repo.get_stories()


        assert result["success"] is False

        assert result["message"] == (
            "No tokenized stories found for category 'Unknown'."
        )


        repo.collection.find.assert_called_once_with(
            {
                "category": "Unknown"
            }
        )



    def test_get_stories_empty_category(self):

        repo = GetTokenizedStoriesByCategoryFromMongoDB(
            ""
        )

        repo.collection = MagicMock()

        repo.collection.find.return_value = []


        result = repo.get_stories()


        assert result["success"] is False

        assert (
            "No tokenized stories found"
            in result["message"]
        )



    def test_get_stories_database_returns_multiple_documents(self):

        repo = GetTokenizedStoriesByCategoryFromMongoDB(
            "Hitopadesha"
        )

        repo.collection = MagicMock()

        stories = [
            {
                "_id": str(i),
                "title": f"Story {i}",
                "category": "Hitopadesha"
            }
            for i in range(5)
        ]


        repo.collection.find.return_value = stories


        result = repo.get_stories()


        assert result["success"] is True

        assert result["count"] == 5

        assert len(result["data"]) == 5