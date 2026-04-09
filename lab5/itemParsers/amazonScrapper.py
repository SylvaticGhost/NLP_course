from bs4 import BeautifulSoup
from lab5.itemParsers.shopScrapper import ShopScrapper


class AmazonScrapper(ShopScrapper):
    async def scrap_async(self, item_url: str) -> str | None:
        html_content = await self._load_html_by_url(item_url)
        if html_content is None:
            print(f'Failed to load HTML for url: {item_url}')
            return None

        soup = BeautifulSoup(html_content, 'html.parser')
        feature_block = soup.find('div', id='feature-bullets')
        bullets_text = []

        if feature_block:
            list_items = feature_block.find_all('li')

            for li in list_items:
                text = li.get_text(strip=True)
                if text:
                    bullets_text.append(text)

        combined_text = " ".join(bullets_text)
        return combined_text