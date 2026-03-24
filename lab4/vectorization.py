import duckdb
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse as sp
import joblib
from pathlib import Path

models_dir = Path("./models")
models_dir.mkdir(exist_ok=True)
data_dir = Path("./data")

print("1. Завантаження даних з бази...")
con = duckdb.connect(str(data_dir / "products.duckdb"))

query = """
    SELECT id, title, text 
    FROM reviews 
    WHERE (text IS NOT NULL AND text != '') 
       OR (title IS NOT NULL AND title != '')
"""
df = con.execute(query).df()
con.close()

print(f"Завантажено {len(df)} відгуків.")

df['title'] = df['title'].fillna('')
df['text'] = df['text'].fillna('')

df['combined_text'] = df['title'] + " " + df['text']
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words='english',
    ngram_range=(1, 2)
)

tfidf_matrix = vectorizer.fit_transform(df['combined_text'])
sp.save_npz(models_dir / 'tfidf_matrix.npz', tfidf_matrix)
joblib.dump(vectorizer, models_dir / 'tfidf_vectorizer.pkl')
df[['id']].to_csv(models_dir / 'matrix_row_ids.csv', index=False)