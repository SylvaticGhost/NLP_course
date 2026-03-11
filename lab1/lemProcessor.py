import asyncio

import stanza
import re

from scrappers.scrapper import TitlePayload, Source
from therm import Therm


class LemProcessor:
    ALLOWED_POS = {"NOUN", "VERB", "ADJ", "ADV"}
    STOPWORDS = {
        "де", "як", "що", "який", "яка", "яке", "які", "котрий", "котра", "котре", "котрі",
        "я", "ти", "він", "вона", "воно", "ми", "ви", "вони",
        "мене", "мені", "мною", "його", "їй", "їм", "ними", "них",
        "мій", "твій", "його", "її", "наш", "ваш", "їхній",
        "цей", "та", "те", "ці", "той", "та", "те", "ті",
        "один", "одна", "одне", "одні", "два", "дві",
        "весь", "вся", "все", "всі", "будь", "кожен", "кожна", "кожне",
        "і", "або", "чи", "ні", "не", "й", "та", "то", "дак", "то", "чому"
    }

    def __init__(self):
        self.nlp = stanza.Pipeline("uk", processors="tokenize,pos,lemma", use_gpu=True)

    def _is_valid_word(self, word):
        return (
                word.upos in self.ALLOWED_POS
                and word.lemma.lower() not in self.STOPWORDS
                and not re.search(r"\d", word.text)  # без цифр
                and re.search(r"[A-Za-zА-Яа-яЇїІіЄєҐґ]", word.text)  # містить літери
        )

    def _process(self, titles: list[TitlePayload], source: Source) -> list[Therm]:
        result = []

        print(f"Processing {len(titles)} titles for source {source.name}")
        iter = 0
        for title in titles:
            doc = self.nlp(title.text)

            lemmas = [
                word.lemma
                for sent in doc.sentences
                for word in sent.words
                if self._is_valid_word(word)
            ]

            for lemma in lemmas:
                result.append(Therm(word=lemma, source=source, date=title.date))
            iter += 1
            if iter % 100 == 0:
                print(f"Processed {iter} titles")

        return result

    async def process_async(self, titles: list[TitlePayload], source: Source) -> list[Therm]:
        return await asyncio.to_thread(self._process, titles, source)
