from services.sanskrit_samskrutam_metadata_extraction_pipeline.extract_data import RetrieveRawData
import re
from uuid import uuid4
from repository.sanskrit_samskrutam_metadata_repo import WriteMetaData


class GetMetaData:
    def __init__(self):
        self.urls = [
            {
                "url": "https://sanskrit.samskrutam.com/en.literature-stories-01.ashx",
                "title": "story1"
            },
            {
                "url": "https://sanskrit.samskrutam.com/en.literature-stories-02.ashx",
                "title": "story2"
            }
        ]

        self.data = []

    def execute(self):
        """Run the complete metadata extraction pipeline."""
        for source in self.urls:
            raw_data = self._retrieve_data(source["url"])
            extracted = self._extract_data(raw_data, source)
            self.data.extend(extracted)

        self._write_data(self.data)
        return self.data

    def _retrieve_data(self, url):
        """Retrieve PageContentDiv from the URL."""
        return RetrieveRawData(url).data

    def _extract_data(self, soup, source):
        result = []

        stories = soup.find_all("span", class_="contentBold3")
        anchors = soup.find_all("a", attrs={"name": True})

        block = {
            "source": source["title"],
            "source_url": source["url"],
            "stories": []
        }

        for anchor, span in zip(anchors, stories):
            raw = span.get_text(strip=True)

            # Preserve hyphens inside Sanskrit titles
            if "--" in raw:
                sanskrit_title, english_title = raw.split("--", 1)
            elif " - " in raw:
                sanskrit_title, english_title = raw.split(" - ", 1)
            else:
                sanskrit_title = raw
                english_title = ""

            block["stories"].append({
                "_id": str(uuid4()),
                "vendorId": anchor.get("name"),
                "sanskrit_title": sanskrit_title.strip(),
                "english_title": english_title.strip(),
                "used":False
            })

        result.append(block)

        return result

    def _write_data(self, data):
        """Write metadata to disk."""
        req = WriteMetaData(data)
        return req.write()