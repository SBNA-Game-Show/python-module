import re


class NormalizeData:
    """
    Given raw data, extracts Sanskrit and English parts.
    """

    def __init__(self, data):
        if not data:
            raise ValueError("DATA IS NOT PROVIDED TO CONVERT TO JSON")

        self.raw_data = data
        self.data = {}  # This will hold the processed data


    def execute(self):
        self.data = self._split_languages()
        english_title = self._normalize_english_passage(
            self._extract_english_title(self.get_sanskrit())
        )
        sanskrit_title = self._extract_sanskrit_title(self.get_sanskrit())
        english_moral = self._normalize_english_passage(
            self._extract_english_moral(self.get_english())
        )
        sanskrit_moral = self._extract_sanskrit_moral(self.get_sanskrit())
        english_passage = self._normalize_english_passage(
            self._extract_english_passage(self.get_english())
        )
        sanskrit_passage = self._normalize_sanskrit_passage(
            self._extract_sanskrit_passage(
                self.get_sanskrit())
        )
        
        return{
            "title":{
                "english_version":english_title,
                "sanskrit_version":sanskrit_title,                
            },
            "storyMoral":[english_moral,sanskrit_moral],
            "englishVersion":english_passage,
            "sanskritVersion":sanskrit_passage
        }
        
        
        
        

    def _split_languages(self):
        parts = re.split(r"\n\s*--\s*\n", self.raw_data, maxsplit=1)

        if len(parts) != 2:
            return {
                "sanskrit": self.raw_data.strip(),
                "english": ""
            }

        return {
            "sanskrit": parts[0].strip(),
            "english": parts[1].strip()
        }

    def get_sanskrit(self):
        return self.data.get("sanskrit")

    def get_english(self):
        return self.data.get("english")
    
    def _extract_sanskrit_title(self,sanskrit_text):
        lines = [l.strip() for l in sanskrit_text.split("\n") if l.strip()]
        if not lines:
            return ""

        title_line = lines[0]

        # Only normalize dashes that have spaces around them or are en/em dashes
        # This leaves internal word hyphens like 'बक-नकुल-कथा' untouched
        title_line = re.sub(r"\s+[-–—]+\s+|\s*[\u2013\u2014]\s*", " - ", title_line)

        parts = title_line.rsplit(" - ", 1)  # split from RIGHT

        return parts[0].strip()
    
    def _extract_english_title(self,english_text):
        lines = [l.strip() for l in english_text.split("\n") if l.strip()]
        if not lines:
            return ""

        title_line = lines[0]

        # Apply the exact same separator normalization
        title_line = re.sub(r"\s+[-–—]+\s+|\s*[\u2013\u2014]\s*", " - ", title_line)

        parts = title_line.rsplit(" - ", 1)

        if len(parts) == 2:
            return parts[1].strip()

        return ""
   
    def _extract_english_moral(self, english_text):
            lines = [l.strip() for l in english_text.split("\n") if l.strip()]
            if not lines:
                return ""

            moral_lines = []
            for line in lines:
                moral_lines.append(line)
                # STRATEGY: A moral paragraph ends explicitly when it finishes with a period,
                # exclamation, or a closing quote following punctuation.
                if (
                    line.endswith(".")
                    or line.endswith('"')
                    or line.endswith('."')
                    or line.endswith('!"')
                ):
                    # Stop immediately after compiling the true introductory block
                    break

            return "\n".join(moral_lines)

    def _extract_english_passage(self, english_text):
            lines = [l.strip() for l in english_text.split("\n") if l.strip()]
            if not lines:
                return ""

            # Find the precise boundary index directly after the moral paragraph breaks
            start_index = 0
            for i, line in enumerate(lines):
                if (
                    line.endswith(".")
                    or line.endswith('"')
                    or line.endswith('."')
                    or line.endswith('!"')
                ):
                    start_index = i + 1
                    break

            return "\n".join(lines[start_index:])
   
   
    def _extract_sanskrit_moral(self, sanskrit_text):
            lines = [l.strip() for l in sanskrit_text.split("\n") if l.strip()]
            if len(lines) < 2:
                return ""

            moral_lines = []
            # The moral starts at index 1 (line 2). It's typically 1 line long.
            for line in lines[1:]:
                moral_lines.append(line)
                # Break if we hit explicitly defined dandas, OR if we've gathered
                # the short introduction sentence before narrative shift
                if "॥" in line or "।" in line or len(moral_lines) >= 1:
                    break

            return "\n".join(moral_lines)
    
    def _extract_english_passage(self, english_text):
            lines = [l.strip() for l in english_text.split("\n") if l.strip()]
            if not lines:
                return ""

            # Find the boundary index right after the moral ends
            start_index = 0
            for i, line in enumerate(lines):
                if (
                    line.endswith(".")
                    or line.endswith('"')
                    or line.endswith("'")
                    or line.endswith('."')
                ):
                    start_index = i + 1
                    break

            return "\n".join(lines[start_index:])
    
    def _extract_sanskrit_passage(self, sanskrit_text):
            lines = [l.strip() for l in sanskrit_text.split("\n") if l.strip()]
            if len(lines) < 2:
                return ""

            # Find where the moral section stops
            start_index = 1
            for i, line in enumerate(lines[1:], start=1):
                if "॥" in line or "।" in line or i == 1:
                    start_index = i + 1
                    break

            return "\n".join(lines[start_index:])
    
    def _normalize_sanskrit_passage(self, passage):
        # Convert list to a single string if it arrives as a list
        if isinstance(passage, list):
            passage = " ".join(passage)

        if isinstance(passage, str):
            # Split by either a single danda (।) or double danda (॥)
            sentences = re.split(r"[।॥]", passage)

            # Clean up whitespace and filter out any empty strings
            cleaned_sentences = []
            for s in sentences:
                stripped = s.strip()
                if stripped:
                    # Optional: Append the danda back to the sentence if you want to keep it
                    cleaned_sentences.append(stripped + " ।")

            return cleaned_sentences

        return []
    
    def _normalize_english_passage(self, passage):
        if not passage:
            return ""

        # 1. Remove literal quotation marks (this cleans up the internal escaped quotes)
        text = passage.replace('"', "")

        # 2. Replace newlines with a space to keep words from sticking together
        text = text.replace("\n", " ")

        # 3. Collapse multiple spaces down to a single space
        return re.sub(r"\s+", " ", text).strip()
    
    