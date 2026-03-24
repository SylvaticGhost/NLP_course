import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import duckdb
import stanza
import json
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from pathlib import Path

cache_dir = Path("./models")
cache_dir.mkdir(exist_ok=True)
data_dir = Path("./data")

con = duckdb.connect(str(data_dir / "products.duckdb"))
query = """
    SELECT title, text 
    FROM reviews 
    WHERE (text IS NOT NULL AND text != '') 
       OR (title IS NOT NULL AND title != '')
"""
df = con.execute(query).df()
con.close()

df['title'] = df['title'].fillna('')
df['text'] = df['text'].fillna('')

df['combined_text'] = df['title'] + " " + df['text']
full_text = " ".join(df['combined_text'].tolist())

nlp = stanza.Pipeline('en', processors='tokenize', use_gpu=True, verbose=True)
doc = nlp(full_text)

words = []
filtered_words = []

for sentence in doc.sentences:
    for token in sentence.tokens:
        word_text = token.text.lower()
        if word_text.isalpha():
            words.append(word_text)
            if word_text not in ENGLISH_STOP_WORDS:
                filtered_words.append(word_text)

cache_data = {
    "words": words,
    "filtered_words": filtered_words
}

with open(cache_dir / 'stanza_cache.json', 'w', encoding='utf-8') as f:
    json.dump(cache_data, f)

print(f"Оброблено {len(words)} слів. Збереженно у файл.")
