import pandas as pd
from deep_translator import GoogleTranslator

df = pd.read_csv('words-not-translated.csv')

translator = GoogleTranslator(source='en', target='uk')

translate_cache = {}

def translate(text):
    if text in translate_cache:
        return translate_cache[text], True

    try:
        translated = translator.translate(text)
        translate_cache[text] = translated
        return translated, True
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return text, False

for index, row in df.iterrows():
    if index % 100 == 0:
        print(f"Translating row {index}/{len(df)}")

    if row['language'] == 'en' or row['language'] == 'et':
        translation, success = translate(row['word'])
        if success:
            df.at[index, 'word'] = translation
            df.at[index, 'language'] = 'uk'

df.to_csv('words-translated.csv', index=False)
