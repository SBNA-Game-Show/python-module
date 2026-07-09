from flask import Blueprint
from flasgger import swag_from


from controller.dictionary_controller import tokenize_english_word, tokenize_sanskrit_word, tokenize_sanskrit_passage


dictionary_bp = Blueprint("dictionary_bp",__name__)


# Get Route to tokenize english word with parts of speech and synonyms and antonyms

decorated_english_controller = swag_from("../swaggerdocs/dictionary/process_english_word.yml")(tokenize_english_word)
dictionary_bp.route("/getEnglish",methods=["GET"])(decorated_english_controller)

decorated_sanskrit_controller = swag_from("../swaggerdocs/dictionary/process_sanskrit_word.yml")(tokenize_sanskrit_word)
dictionary_bp.route("/getSanskrit",methods=["GET"])(decorated_sanskrit_controller)

decorated_sanskrit_passage_controller = swag_from("../swaggerdocs/dictionary/process_sanskrit_passage.yml")(tokenize_sanskrit_passage)
dictionary_bp.route("/tok-passage",methods=["POST"])(decorated_sanskrit_passage_controller)
