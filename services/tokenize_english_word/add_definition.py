import nltk
from nltk.corpus import wordnet


class AddDefinition:
    def __init__(self,word):
        if not word:
            raise ValueError("English wword is required")
        self.word = word.lower()
        
    def get_definition(self):
        
        synsets = wordnet.synsets(self.word)
        
        definition = synsets[0].definition() 
        
        return definition
        
        