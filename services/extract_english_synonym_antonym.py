from services.tokenize_english_word.get_synonyms import GetSynonyms
from services.tokenize_english_word.get_antonyms import GetAntonyms


class ExtractEnglishSynonymAntonym:
    """Extract synonyms and antonyms using WordNet"""

    def __init__(self, data):
        self.data = data


    def _extract_data(self):

        return self.data.get(
            "tokenized_english_version",
            []
        )


    def execute(self):

        tokens = self._extract_data()


        for token in tokens:

            token["synonyms"] = (
                GetSynonyms(token).execute()
            )

            token["antonyms"] = (
                GetAntonyms(token).execute()
            )


        return self.data