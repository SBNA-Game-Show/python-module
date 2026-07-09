import re

class DharmamitraExtractor:

    POS_TAGS = {
        "noun": "NOUN",
        "pronoun": "PRON",
        "verb": "VERB",
        "adjective": "ADJ",
        "adverb": "ADV",
        "particle": "PART",
        "conjunction": "CCONJ",
        "indeclinable": "PART",
        "gerund": "VERB",
        "infinitive": "VERB",
        "participle": "VERB",
        "numeral": "NUM",
        "preposition": "ADP"
    }

    def is_devanagari(self, text):
        # Quick helper to see if a string contains Devanagari script characters
        return bool(re.search(r'[\u0900-\u097F]', text))

    def extract(self, raw_text):

        results = []

        # ------------------------------------------------------------------
        # Process line-by-line instead of capturing whole blocks.
        # Word entries always begin with:
        #
        # * **WORD**
        #
        # Ignore English and Sanskrit sentence lines.
        # ------------------------------------------------------------------

        for line in raw_text.splitlines():

            line = line.strip()

            if not re.match(r'^\*\s+\*\*', line):
                continue

            # --------------------------------------------------------------
            # Extract definition
            # --------------------------------------------------------------

            definition_match = re.search(r'_(.*?)_', line)
            definition = definition_match.group(1).strip() if definition_match else ""

            line = re.sub(r'_(.*?)_', '', line)

            # --------------------------------------------------------------
            # Extract the word inside **
            # --------------------------------------------------------------

            word_match = re.search(r'\*\*(.*?)\*\*', line)

            if not word_match:
                continue

            word = word_match.group(1).strip()

            # Remove markdown prefix
            remainder = re.sub(r'^\*\s+\*\*.*?\*\*', '', line)
            remainder = remainder.strip(" ,.")

            # Remove parentheses
            remainder = (
                remainder
                .replace("(", "")
                .replace(")", "")
                .replace(".", "")
            )

            fields = [x.strip() for x in remainder.split(",") if x.strip()]

            lemma = None
            upos = "X"
            features = ""

            # --------------------------------------------------------------
            # Find POS
            # --------------------------------------------------------------

            pos_index = None
            pos_name = None

            for i, field in enumerate(fields):

                lower = field.lower()

                for pos in self.POS_TAGS:

                    if re.search(rf"\b{re.escape(pos)}\b", lower):
                        pos_index = i
                        pos_name = pos
                        break

                if pos_index is not None:
                    break

            # --------------------------------------------------------------
            # Lemma
            # --------------------------------------------------------------

            if pos_index is not None:

                before = fields[:pos_index]

                if before:

                    # Case:
                    # sa
                    # pronoun
                    #
                    # or
                    #
                    # śaśaka
                    # śaśakaḥ
                    # noun

                    devanagari = [x for x in before if self.is_devanagari(x)]

                    if devanagari:
                        lemma = devanagari[0]
                    else:
                        lemma = before[0]

                upos = self.POS_TAGS[pos_name]

                # ----------------------------------------------------------
                # Features
                # ----------------------------------------------------------

                if len(fields) > pos_index + 1:

                    features = ", ".join(fields[pos_index + 1:])

                else:
                    # POS embedded inside feature field
                    features = fields[pos_index]

                    features = re.sub(
                        r'\b(noun|verb|pronoun|adjective|adverb|particle|'
                        r'conjunction|indeclinable|gerund|infinitive|'
                        r'participle|numeral|preposition)\b',
                        '',
                        features,
                        flags=re.I
                    ).strip(" ,")

            else:

                # fallback
                lemma = word

            # --------------------------------------------------------------
            # If word is transliterated and lemma is Devanagari, swap them
            # --------------------------------------------------------------

            if lemma and self.is_devanagari(lemma) and not self.is_devanagari(word):
                word, lemma = lemma, word

            results.append(
                {
                    "text": word,
                    "lemma": lemma,
                    "upos": upos,
                    "features": features,
                    "definition": definition
                }
            )

        return results