from bs4 import BeautifulSoup
import requests
import urllib3
import time
import json
from uuid import uuid4
from datetime import datetime

class RetrieveMetaData:

    def __init__(self):
        self.url = "https://learnsanskrit.cc/fables/getFables"
        urllib3.disable_warnings(
            urllib3.exceptions.InsecureRequestWarning
        )

    def _send_request(self):
        response = requests.get(
            self.url,
            verify=False,
        )
        response.raise_for_status()
        return response

    def _parse_request(self, raw_data):
        soup = BeautifulSoup(
            raw_data.text,
            "html.parser"
        )
        return {
            "title": (
                soup.title.string
                if soup.title
                else None
            )
        }

    def _extract_vendor_id(self, raw_data):
        soup = BeautifulSoup(
            raw_data.text,
            "html.parser"
        )
        jpg_names = []
        img_tags = soup.find_all("img")

        for img in img_tags:
            src = img.get("src")
            if src:
                src = (
                    src.replace('\\"', '')
                       .replace('"', '')
                       .strip()
                       .strip(',')
                )
                filename = src.split("/")[-1]
                if filename.lower().endswith(".jpg"):
                    jpg_names.append(filename)

        cleaned_vendor_id = [
            name.replace("_icon.jpg", "")
            for name in jpg_names
        ]
        return cleaned_vendor_id

    def _extract_fable_description(self, raw_data):
        results = []
        soup = BeautifulSoup(
            raw_data.text,
            "html.parser"
        )
        story_description = soup.find_all(
            class_='\\"fabdeclaration\\"'
        )

        if not story_description:
            story_description = soup.find_all(
                class_="fabdeclaration"
            )

        for item in story_description:
            title_tag = item.find(["b", "strong"])
            title = (
                title_tag.get_text(strip=True)
                if title_tag
                else "Unknown"
            )

            if title_tag:
                title_tag.extract()

            description = item.get_text(" ", strip=True)

            results.append({
                "title": title,
                "description": description
            })

        return results

    def _generate_base_url(self, vendor_id):
        return (
            "https://learnsanskrit.cc/"
            f"fables/story?name={vendor_id}"
            f"&active=true"
        )

    def _extract_story_metadata(self, cleaned_vendor_id):
        complete_page = []
        for story_id in cleaned_vendor_id:
            url = self._generate_base_url(story_id)
            response = requests.get(
                url,
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            complete_data = response.json()
            complete_page.append(complete_data)
            
            # Be polite to the server

        return complete_page

    def _normalize_title(self, title, description):
        if title != "Unknown":
            return title
        if "Panchatantra" in description:
            return "Panchatantra"
        return title

    def _build_final_result(self, results, cleaned_vendor_id, complete_page):
        category_map = {}

        # -----------------------------------
        # STEP 1: CREATE CATEGORY STRUCTURE
        # -----------------------------------
        for item in results:
            title = item.get("title", "").strip()

            category_map[title] = {
                "_id": str(uuid4()),
                "title": title,
                "description": item.get("description", ""),
                "origin": title,  # Will dynamically adapt to "Panchatantra" now
                "story_description": []
            }

        # -----------------------------------
        # STEP 2: ADD STORIES TO CATEGORY
        # -----------------------------------
        for vendor_id, page_data in zip(cleaned_vendor_id, complete_page):
            data = page_data.get("data", {})
            author = data.get("author", "").strip()
            summary_head = data.get("summary_head", [])
            story_title = summary_head[0] if summary_head else ""

            story_object = {
                "_id": str(uuid4()),
                "vendorId": vendor_id,
                "storyTitle": story_title,
                "used": False,
                "updatedOn": datetime.utcnow().isoformat()
            }

            # Now 'author' (e.g., "Panchatantra") properly matches our mapping key
            if author in category_map:
                category_map[author]["story_description"].append(story_object)

        # -----------------------------------
        # STEP 3: CONVERT TO ARRAY
        # -----------------------------------
        return list(category_map.values())

    def execute(self):
        raw_data = self._send_request()
        cleaned_vendor_id = self._extract_vendor_id(raw_data)
        
        # Get raw fables metadata
        raw_results = self._extract_fable_description(raw_data)
        
        # FIX 1: Run your normalization loop to intercept "Unknown" titles
        normalized_results = []
        for item in raw_results:
            clean_title = self._normalize_title(item["title"], item["description"])
            normalized_results.append({
                "title": clean_title,
                "description": item["description"]
            })

        complete_page = self._extract_story_metadata(cleaned_vendor_id)

        # FIX 2: Pass 'normalized_results' into build payload mapper
        final_result = self._build_final_result(
            normalized_results,
            cleaned_vendor_id,
            complete_page
        )

        return final_result