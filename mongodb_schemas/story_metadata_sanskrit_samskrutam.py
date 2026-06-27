from config.dbconfig import connect_db

db = connect_db()

samskrutam_metadata_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "source",
            "source_url",
            "stories",
            "createdAt"
        ],
        "properties": {

            "source": {
                "bsonType": "string",
                "description": "Name of the source page (story1, story2, ...)"
            },

            "source_url": {
                "bsonType": "string",
                "description": "URL from which the metadata was extracted"
            },

            "createdAt": {
                "bsonType": "date"
            },

            "stories": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": [
                        "_id",
                        "vendorId",
                        "sanskrit_title",
                        "english_title"
                    ],
                    "properties": {

                        "_id": {
                            "bsonType": "string"
                        },

                        "vendorId": {
                            "bsonType": "string"
                        },

                        "sanskrit_title": {
                            "bsonType": "string"
                        },

                        "english_title": {
                            "bsonType": "string"
                        },

                        "used": {
                            "bsonType": "bool"
                        }
                    }
                }
            }
        }
    }
}

db.create_collection(
    "samskrutam_metadata",
    validator=samskrutam_metadata_validator
)