from config.dbconfig import connect_db

db = connect_db()
learnsanskrit_metadata_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "_id",
            "title",
            "description",
            "origin",
            "story_description",
            "createdAt"
        ],
        "properties": {
            "_id": {
                "bsonType": "string"
            },

            "title": {
                "bsonType": "string"
            },

            "description": {
                "bsonType": "string"
            },

            "origin": {
                "bsonType": "string"
            },

            "createdAt": {
                "bsonType": "date"
            },

            "story_description": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": [
                        "_id",
                        "vendorId",
                        "storyTitle",
                        "used"
                    ],
                    "properties": {
                        "_id": {
                            "bsonType": "string"
                        },

                        "vendorId": {
                            "bsonType": "string"
                        },

                        "storyTitle": {
                            "bsonType": "string"
                        },

                        "used": {
                            "bsonType": "bool"
                        },

                        "updatedOn": {
                            "bsonType": ["date", "null"]
                        }
                    }
                }
            }
        }
    }
}

db.create_collection(
    "learnsank_meta",
    learnsanskrit_metadata_validator
    
)