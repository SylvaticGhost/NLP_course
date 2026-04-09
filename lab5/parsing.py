import asyncio

from lab5.itemParsers.amazonScrapper import AmazonScrapper
from lab5.itemParsers.ebayScrapper import EbayScrapper
from lab5.itemParsers.itemScrappStrategy import ItemScrappStrategy

scraper = EbayScrapper()
source = 'ebay'

strategy = ItemScrappStrategy(source, scraper)
asyncio.run(strategy.load())
