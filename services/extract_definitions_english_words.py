from nltk.corpus import wordnet


class ExtractDefinitions:

    def __init__(self, data):
        self.data = data


    def _extract_data(self):

        return self.data.get(
            "tokenized_english_version",
            []
        )


    def execute(self):

        tokens = self._extract_data()


        for item in tokens:

            word = item.get(
                "lemma",
                ""
            )

            synsets = wordnet.synsets(
                word
            )

            item["definition"] = (
                synsets[0].definition()
                if synsets
                else None
            )


        return self.data