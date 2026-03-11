import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import asyncio
from datetime import datetime, timedelta

from lab1.lemProcessor import LemProcessor
from lab1.scrappers.scrapper import TitlePayload
from lab1.scrappers.rbcScrapper import RbcScrapper
from termOccurenceRepository import TermOccurrenceRepository
from therm import Therm
from lab1.scrappers.upScrapper import UpScrapper


up_scrapper = UpScrapper()
rbc_scrapper = RbcScrapper()

current_date = datetime.now()
end_date = current_date - timedelta(days=3)
start_date = current_date - timedelta(days=155)

print(f"Start scrapping for source {up_scrapper.source.name}")
content: list[TitlePayload] = asyncio.run(up_scrapper.scrap_async(start_date, end_date))
rbc_content: list[TitlePayload] = asyncio.run(rbc_scrapper.scrap_async(start_date, end_date))
print(f"Processing content for lemmatization")

lemProcessor = LemProcessor()
terms: list[Therm] = asyncio.run(lemProcessor.process_async(content, up_scrapper.source))
rbc_terms: list[Therm] = asyncio.run(lemProcessor.process_async(rbc_content, rbc_scrapper.source))

terms.extend(rbc_terms)

print(f"Saving term occurrences to database")

occurence_repo = TermOccurrenceRepository()
occurence_repo.save_therms(terms)
