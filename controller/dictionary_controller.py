import re
from flask import jsonify,request

from services.tokenize_english_word.process_english_word import ProcessEnglishWord
from services.tokenize_sanskrit_word.tokenize_sanskrit_word import TokenizeSanskritWord
from services.tokenize_sanskrit_passage_web import TokenizeSanskritPassageWeb

## given a english word provides what it is and its synonyms and antonyms
def tokenize_english_word():
    word = request.args.get("word")
        
    if not word:
        return jsonify({
        "success":False,
        "message":"English Word is required"
        }),400
        
    service = ProcessEnglishWord(word)
    data = service.tokenize()
    
    return jsonify({
        "success":True,
        "data":data
    })

## given a sanskrit word provides noun, verb or adjective

def tokenize_sanskrit_word():
    word = request.args.get("word")
    
    if not word:
        return jsonify({
        "success":False,
        "message":"English Word is required"
        }),400
        
    tokenizer = TokenizeSanskritWord(word)
    data = tokenizer.tokenize()
    
    return({
        "success":True,
        "data":data
    })
    
def is_devanagari(text):
    """
    Check whether text contains Devanagari Unicode characters.
    """
    return bool(re.search(r'[\u0900-\u097F]', text))
    
## given a sanskrit passage the endpoint tokenizes and returns tokenized unique word array

def tokenize_sanskrit_passage():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Sanskrit passage is required"
        }), 400


    if not isinstance(data, list):
        return jsonify({
            "success": False,
            "message": "Expected JSON array of Sanskrit sentences"
        }), 400


    normalized_data = {
        "sanskritVersion": data
    }


    service = TokenizeSanskritPassageWeb(normalized_data)

    result = service.tokenize()


    return jsonify({
        "success": True,
        "data": result
    }), 200

    
    