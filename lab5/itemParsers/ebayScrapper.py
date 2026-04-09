from bs4 import BeautifulSoup
import re
from lab5.itemParsers.shopScrapper import ShopScrapper


class EbayScrapper(ShopScrapper):
    async def scrap_async(self, item_url: str) -> str | None:
        match = re.search(r'/itm/(\d+)', item_url)
        if not match:
            print(f'Failed to find item ID in {item_url}')
            return None

        item_id = match.group(1)
        desc_url = f"https://itm.ebaydesc.com/itmdesc/{item_id}"
        iframe_html_content = await self._load_html_by_url(desc_url)

        if not iframe_html_content:
            print(f'Failed to load direct description for {item_id}')
            return None

        if ("captcha" in iframe_html_content.lower() or
                "security" in iframe_html_content.lower()):
            print(f'Caught CAPTCHA on description endpoint for {item_id}')
            return None

        iframe_soup = BeautifulSoup(iframe_html_content, 'html.parser')
        for script_or_style in iframe_soup(['script', 'style']):
            script_or_style.decompose()

        return iframe_soup.get_text(separator=' ', strip=True)
