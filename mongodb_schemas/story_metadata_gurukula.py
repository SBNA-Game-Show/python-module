from config.dbconfig import connect_db

db = connect_db()

gurukula_metadata_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "createdAt",
            "categories"
        ],
        "properties": {

            "createdAt": {
                "bsonType": "date"
            },

            "categories": {
                "bsonType": "object",
                "description": "Dictionary of Gurukula categories",
                "additionalProperties": {
                    "bsonType": "object",
                    "required": [
                        "category_link",
                        "stories"
                    ],
                    "properties": {

                        "category_link": {
                            "bsonType": "string"
                        },

                        "stories": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "object",
                                "required": [
                                    "_id",
                                    "story_url",
                                    "title",
                                    "used"
                                ],
                                "properties": {

                                    "_id": {
                                        "bsonType": "string"
                                    },

                                    "story_url": {
                                        "bsonType": "string"
                                    },

                                    "title": {
                                        "bsonType": "string"
                                    },

                                    "used": {
                                        "bsonType": "bool"
                                    },
                                    "usedDate": {
                                        "bsonType": ["date", "null"]
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

db.create_collection(
    "gurukula_metadata",
    validator=gurukula_metadata_validator
)