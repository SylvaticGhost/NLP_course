import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer

BASE_MODELS_DIR = "E:/Uni/Models"
os.makedirs(BASE_MODELS_DIR, exist_ok=True)

distilbert_name = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
DISTILBERT_PATH = os.path.join(BASE_MODELS_DIR, "distilbert-sst2")

tokenizer = AutoTokenizer.from_pretrained(distilbert_name)
model = AutoModelForSequenceClassification.from_pretrained(distilbert_name)

tokenizer.save_pretrained(DISTILBERT_PATH)
model.save_pretrained(DISTILBERT_PATH)

minilm_name = "all-MiniLM-L6-v2"
MINILM_LOCAL_PATH = os.path.join(BASE_MODELS_DIR, minilm_name)

st_model = SentenceTransformer(minilm_name)
st_model.save(MINILM_LOCAL_PATH)
