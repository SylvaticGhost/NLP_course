import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import pandas as pd
import stanza
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import re
from tqdm import tqdm

tqdm.pandas(desc='Tokenizing and lemmatizing')

df_amazon = pd.read_csv('./offtop/amazon_text.csv')
df_wayfair = pd.read_csv('./offtop/wayfair_text.csv')
df_ebay = pd.read_csv('./offtop/ebay_text.csv')

df_amazon['platform'] = 'amazon'
df_wayfair['platform'] = 'wayfair'
df_ebay['platform'] = 'ebay'

df = pd.concat([df_amazon, df_wayfair, df_ebay])
print(f"Початкова кількість рядків: {len(df)}")

df = df.dropna(subset=['text'])

df['text'] = df['text'].astype(str).str.replace(r'\xa0', ' ', regex=True)
df['text'] = df['text'].str.replace(r'&nbsp;', ' ', regex=True)


def clean_artifacts(text):
    text = re.sub(r'^eBay\W*', '', text, flags=re.IGNORECASE)
    text = text.replace('About This Product', ' ')
    text = text.replace('Features', ' ')
    return text.strip()

df['text'] = df['text'].apply(clean_artifacts)
df = df.drop_duplicates(subset=['text'], keep='first')
df = df[df['text'].str.len() > 1]
print(f"Кількість унікальних текстів після очистки дублікатів: {len(df)}")

print("Завантаження моделі Stanza для англійської мови...")
nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma', use_gpu=True)

def clean_and_lemmatize(text):
    doc = nlp(text)
    cleaned_tokens = []

    for sentence in doc.sentences:
        for word in sentence.words:
            lemma = word.lemma.lower() if word.lemma else word.text.lower()

            if lemma.isalpha() and lemma not in ENGLISH_STOP_WORDS:
                cleaned_tokens.append(lemma)

    return " ".join(cleaned_tokens)

print(f"Починаємо токенізацію та лематизацію {len(df)} текстів...")
df['cleaned_tokens'] = df['text'].progress_apply(clean_and_lemmatize)

output_file = "ecommerce_unified_dataset_clean.csv"
df.to_csv(output_file, index=False)