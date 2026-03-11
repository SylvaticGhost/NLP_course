import asyncio
import pandas as pd

from lab2.djinniScrapper import DjinniTitleScrapper

scraper = DjinniTitleScrapper()
titles = asyncio.run(scraper.scrap_async())

df = pd.DataFrame(titles, columns=["Title", "URL"])
df.to_csv("djinni_titles.csv", index=False)
