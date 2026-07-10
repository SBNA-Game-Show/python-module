import re
from uuid import uuid4
from datetime import datetime

from services.gurukula.meta_data.extract_category import ExtractCategory
from services.gurukula.meta_data.extract_story_list import ExtractStoryList
from repository.gurukula_metadata_repo import WriteMetaData


class ExtractGuruKulaMetaData:

    def __init__(self):
        self.story_list = []
        self.unwanted_stories =["/parichayah"]
        self.unwanted_categories=[
            "/sa/raghuvamsham",
            "/sa/nava-mishrita-gitani",
            "/sa/vedika-samskritagitani",
            "/sa/bhagavad-gita-padmakumar",
            "/sa/mundakopanishat",
            "/sa/vibhakti",
            "/sa/sankhya-visheshanani",
            "/sa/namapadani",
            "/sa/sandhi",
            "/sa/samasa",
            "/sa/karakam",
            "/sa/pakavani-samskritam",
            "/sa/raghuvamsham",
        ]


    def execute(self):

        categories = ExtractCategory().extract()

        for category in categories:
            link = category["category_link"]

            stories = ExtractStoryList(link).execute()

            self.story_list.extend(stories)


        if not self.story_list:
            raise RuntimeError(
                "Unable to extract story list from categories"
            )


        raw_data = self._mapper(
            categories,
            self.story_list
        )

        cleaned_data = self._clean_data(raw_data)
        
        final_data = self._remove_extra_data(cleaned_data)
        
        final_result = self._write_to_db(final_data)

        return final_result


    def _mapper(self, categories, story_list):

        master_data = {
            "categories":{}
        }

        # Create categories
        for category in categories:

            category_name = category["category"]

            master_data["categories"][category_name] = {
                "category_link": category["category_link"],
                "stories": []
            }


        # Assign stories
        for category_name, category_data in master_data["categories"].items():

            category_link = category_data["category_link"]

            for story in story_list:

                if story["url"].startswith(category_link + "/"):

                    category_data["stories"].append({
                        "_id": str(uuid4()),
                        "story_url": story["url"],
                        "title": story["text"],
                        "used":False,
                        "usedDate":None
                    })


        return master_data


    def _clean_data(self, data):

        for _, category_data in data["categories"].items():

            for story in category_data["stories"]:

                story["title"] = re.sub(
                    r"^\d+\.\s*",
                    "",
                    story["title"]
                ).strip()

        return data
    
    def _remove_extra_data(self, data):

        # Remove unwanted categories
        remove_keys = []

        for category_name, category_data in data["categories"].items():

            if category_data["category_link"] in self.unwanted_categories:
                remove_keys.append(category_name)
                continue

            # Remove unwanted stories
            category_data["stories"] = [
                story
                for story in category_data["stories"]
                if not any(
                    unwanted in story["story_url"]
                    for unwanted in self.unwanted_stories
                )
            ]

        for key in remove_keys:
            del data["categories"][key]

        return data
    
    def _write_to_db(self,data):
        result = WriteMetaData(data)
        return result.write()
    
    