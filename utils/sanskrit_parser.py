from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


class SanskritToTransliterate:
    
    def __init__(self,sentence):
        if not sentence:
            raise ValueError("Sentence is Required")
        self.sentence = sentence
 
        
    
    def transliterate(self):
        sentence = sanscript.transliterate(
            self.sentence,
            sanscript.DEVANAGARI,
            sanscript.IAST
            )
        
        return sentence
    
class TransliterateToSanskrit:
    def __init__(self,sentence):
        if not sentence:
            raise ValueError("Sentence is Required")
        self.sentence = sentence
        
    def translate(self):
        sentence = sanscript.transliterate(
            self.sentence,
            sanscript.IAST,
            sanscript.DEVANAGARI
            
        )
        
        return sentence

    