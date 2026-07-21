
import spacy

_nlp = None

def get_spacy():
    global _nlp

    if _nlp is None:
        print("Loading spaCy model...")
        _nlp = spacy.load("en_core_web_sm")

    return _nlp