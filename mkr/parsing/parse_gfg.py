import asyncio
import json
import os

from mkr.parsing.geeksForGeeksScrapper import GeeksForGeeksScrapper

URLS = [
    "https://www.geeksforgeeks.org/nlp/what-is-tokenization/",
    "https://www.geeksforgeeks.org/nlp/removing-stop-words-nltk-python/",
    "https://www.geeksforgeeks.org/nlp/how-to-remove-punctuations-in-nltk/",
    "https://www.geeksforgeeks.org/machine-learning/introduction-to-stemming/",
    "https://www.geeksforgeeks.org/python/python-lemmatization-with-nltk/",
    "https://www.geeksforgeeks.org/python/normalizing-textual-data-with-python/",
    "https://www.geeksforgeeks.org/nlp/nlp-part-of-speech-default-tagging/",
    "https://www.geeksforgeeks.org/compiler-design/introduction-of-parsing-ambiguity-and-parsers-set-1/"
]


async def main():
    scrapper = GeeksForGeeksScrapper()
    all_chunks = []

    for url in URLS:
        chunks = await scrapper.get_article_chunks(url)

        if chunks:
            print(f"Успішно! Знайдено {len(chunks)} чанків.")
            all_chunks.extend(chunks)
        else:
            print("Не вдалося розпарсити статтю.")

    os.makedirs("./../volume", exist_ok=True)
    output_path = "./../volume/nlp_reference_materials.json"

    serialized_data = []
    for chunk in all_chunks:
        serialized_data.append({
            "page_content": chunk.page_content,
            "metadata": chunk.metadata
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serialized_data, f, ensure_ascii=False, indent=4)

    print(f"\nГотово! {len(all_chunks)} чанків успішно збережено у {output_path}.")

if __name__ == "__main__":
    asyncio.run(main())
