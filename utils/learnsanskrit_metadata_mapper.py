from datetime import datetime


class LearnSanskritMetaDataMapper:

    @staticmethod
    def to_schema(data: dict) -> dict:
        return {
            "_id": data.get("_id"),
            "title": data.get("title"),
            "description": data.get("description"),
            "origin": data.get("origin"),
            "createdAt": datetime.utcnow(),
            "story_description": [
                {
                    "_id": story.get("_id"),
                    "vendorId": story.get("vendorId"),
                    "storyTitle": story.get("storyTitle"),
                    "used": story.get("used", False),
                    "updatedOn": (
                        datetime.fromisoformat(story["updatedOn"])
                        if story.get("updatedOn")
                        else None
                    ),
                }
                for story in data.get("story_description", [])
            ],
        }