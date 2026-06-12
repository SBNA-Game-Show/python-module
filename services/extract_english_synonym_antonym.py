import spacy
import nltk
from nltk.corpus import wordnet

from services.tokenize_english_word.get_synonyms import GetSynonyms
from services.tokenize_english_word.get_antonyms import GetAntonyms


class ExtractEnglishSynonymAntonym:
    """Extract synonyms and antonyms using spaCy + WordNet"""

    def __init__(self, data):
        self.data = data


    def _extract_data(self, data):
        return data.get("tokenized_english_version", [])

     
    

    def execute(self):

            tokens = self._extract_data(self.data)

            enriched_tokens = []

            for token in tokens:

                token_copy = token.copy()

                token_copy["synonyms"] = GetSynonyms(token).execute()
                token_copy["antonyms"] = GetAntonyms(token).execute()

                enriched_tokens.append(token_copy)

            new_data = self.data.copy()
            new_data["tokenized_english_version"] = enriched_tokens

            return new_data