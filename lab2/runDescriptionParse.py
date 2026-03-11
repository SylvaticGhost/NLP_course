import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import stanza
import re
import pandas as pd
from langdetect import detect, DetectorFactory

from lab2.vacancyBodyScraper import VacancyBodyScraper
import asyncio

parser = VacancyBodyScraper()


nlp_urk = stanza.Pipeline("uk", processors="tokenize,pos,lemma", use_gpu=True)
nlp_eng = stanza.Pipeline("en", processors="tokenize,pos,lemma", use_gpu=True)

rows = []

vacancy_df = pd.read_csv('djinni_titles.csv')
for url in vacancy_df['URL']:
    desc = asyncio.run(parser.scrap_async(url))
    if desc is None:
        continue

    try:
        lang = detect(desc)
    except:
        lang = 'en'

    if lang == 'uk':
        doc = nlp_urk(desc)
    else:
        doc = nlp_eng(desc)

    for sentence in doc.sentences:
        for word in sentence.words:
            if re.match(r'^[\w-]+$', word.text):
                lemma = word.lemma.lower()
                rows.append({'word': lemma, 'source': url, 'upos': word.upos, 'original': word.text, 'language': lang})

df_words = pd.DataFrame(rows, columns=['word', 'source', 'upos', 'original', 'language'])
df_words.to_csv('words.csv', index=False)
