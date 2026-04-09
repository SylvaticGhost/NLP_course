from lab5.itemParsers.shopScrapper import ShopScrapper
import pandas as pd

class ItemScrappStrategy:
    def __init__(self, source: str, scrapper: ShopScrapper):
        self.source = source
        self.scrapper = scrapper

    async def load(self):
        url_source = f'./offtop/{self.source}_urls.csv'
        df = pd.read_csv(url_source)

        for index, row in df.iterrows():
            url = row['url']
            text = await self.scrapper.scrap_async(url)
            df.at[index, 'text'] = text
            if index % 10 == 0:
                print(f'{index} / {len(df)}')

        df.to_csv(f'./offtop/{self.source}_text.csv', index=False)