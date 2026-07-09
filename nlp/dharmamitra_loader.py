import os
import torch
from transformers import AutoTokenizer, T5ForConditionalGeneration
from config.envconfig import HF_TOKEN

os.environ["HF_TOKEN"] = HF_TOKEN

model_name = "chronbmm/sanskrit5-multitask"

model = None
tokenizer = None

def load_dharmamitra_model():
    global model, tokenizer

    print("Loading model at startup...")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    print("Model loaded successfully.")

# call this once at startup
load_dharmamitra_model()