from flask import jsonify,request

from services.tokenize_english_word.process_english_word import ProcessEnglishWord
from services.tokenize_sanskrit_word.tokenize_sanskrit_word import TokenizeSanskritWord

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
    
    