import asyncio
from datetime import datetime
import pandas as pd

from lab1.scrappers.scrapper import TitlePayload
from lab1.scrappers.rbcScrapper import RbcScrapper
from lab1.scrappers.upScrapper import UpScrapper

up_scrapper = UpScrapper()
rbc_scrapper = RbcScrapper()

end_date = datetime.strptime("2025-09-14", "%Y-%m-%d")
start_date = datetime.strptime("2026-02-14", "%Y-%m-%d")
print(f"Scrap date range: {start_date} - {end_date}")

up_titles: list[TitlePayload] = asyncio.run(up_scrapper.scrap_async(start_date, end_date))
rbc_titles: list[TitlePayload] = asyncio.run(rbc_scrapper.scrap_async(start_date, end_date))

df_up = pd.DataFrame([{"text": title.text, "date": title.date, "source": "UP"} for title in up_titles])
df_rbc = pd.DataFrame([{"text": title.text, "date": title.date, "source": "RBC"} for title in rbc_titles])

df = pd.concat([df_up, df_rbc], ignore_index=True)
df.to_csv("../data/news_titles.csv", index=False)