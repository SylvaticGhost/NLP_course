from lab2.webScrapper import WebScrapper

from bs4 import BeautifulSoup
from langchain_text_splitters import HTMLHeaderTextSplitter, RecursiveCharacterTextSplitter

class GeeksForGeeksScrapper(WebScrapper):
    @property
    def _call_delay(self) -> float:
        return 1.0

    async def get_article_chunks(self, url: str):
        print(f"Завантаження {url}...")
        html_content = await self._load_html_by_url(url, headers=self.HEADERS)

        if not html_content:
            print("Помилка: Отримано порожній HTML.")
            return []

        soup = BeautifulSoup(html_content, "html.parser")

        h1_tag = soup.find('h1')
        article_title = h1_tag.get_text(strip=True) if h1_tag else "GeeksForGeeks Article"

        article_body = soup.find('div', class_='text')

        if not article_body:
            article_body = soup.find('div', class_='html-chunk')

        if not article_body:
            print("Помилка: Не знайдено основний текстовий блок статті.")
            return []

        for unwanted in article_body.find_all(['iframe', 'script']):
            unwanted.decompose()

        extracted_html = str(article_body)

        headers_to_split_on = [
            ("h2", "Section"),
            ("h3", "Subsection"),
            ("h4", "Sub-subsection")  
        ]

        html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        semantic_chunks = html_splitter.split_text(extracted_html)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )

        final_chunks = text_splitter.split_documents(semantic_chunks)
        for chunk in final_chunks:
            chunk.metadata['Article_Title'] = article_title
            chunk.metadata['Source'] = url

        return final_chunks


    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "uk-UA,uk;q=0.9,en-GB;q=0.8,en;q=0.7,ru-UA;q=0.6,ru;q=0.5,en-US;q=0.4",
        "cache-control": "max-age=0",
        "cookie": "_ga=GA1.1.1524871475.1774652564; gfg_theme=gfgThemeLight; _gcl_au=1.1.1532193622.1774652564; _cc_id=438820578aa699fa48c1c07e21b39013; _gd_visitor=eee6915b-d123-4a37-8690-2d385f618c86; _gd_svisitor=74bd7b5cbe4f000096b2a86965030000cc350000; gfg_nluid=6f3922d1cfd83459931a907aad339fbd; gfg_id5_ipv4=185.42.130.188; gfg_id5_user_agent=Mozilla/5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit/537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome/147.0.0.0%20Safari/537.36; _pubcid=88c411e6-75dd-45ad-acf2-75aa95dffbbd; _pubcid_cst=zix7LPQsHA%3D%3D; _lr_env_src_ats=false; gfg_ads_exp=NO-RUNNING-EXPERIMENTS; gfg_ads_country=UA; panoramaId_expiry=1778055974299; panoramaId=602949b60dbf8ed76cf330725b9ba9fb927ae2604ff2bb7d734d247b0610959d; _gd_session=7db9b359-c024-45e3-878e-783bd97b48a8; _lr_retry_request=true; udsession=e30:1wKCBW:UEoKy_NX-4iIVPn8sK0mq-bMMr9YbB63E5BbeDvH7SI; http_referrer=https://www.geeksforgeeks.org/machine-learning/phases-of-natural-language-processing-nlp/; cto_bundle=FmtvHl9yNXE2RUhITzlsZUVRUHBsSEUzWjJkZjQ1OFZnbFdSd0UwZVhzdWg5YmUydW8yZjRjRlVva2hrelVnanQlMkZBWUI1WU55R2tvT1NNZVQlMkZzQlBoM2UyaUZrZldlN2FDaU5yVUtnUXp0dnVmMkNwclglMkJpUDFHMDZRQWJ6S3R5RGhieSUyRnNGOEI5R3BWVzRvWG5kYlY4cEx0QSUzRCUzRA; cto_bidid=UmEuH18yOXUlMkIxayUyRjhkMjhJU05HSVI1ZjRCd1MyTnJBRVZNTTh4UTY0ZWVybFhuNU9WalhONWtOSEdCd3c1MVBjajR2cmd3aGtSNHJUbWplaCUyRjVVZVNLa24lMkYyQkRQTmtHWVdKOHhXQ2VYelJGWHE4WTlXNng3RTFCbjNKUm1Dbm13VUtk; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%227c074d71-bdca-4486-b860-32aaa695464a%5C%22%2C%5B1774652565%2C22000000%5D%5D%22%5D%5D%5D; FCNEC=%5B%5B%22AKsRol_pbu_T5GI4Gi1IBr7cNsTh0eZxRfcw-GutjVo637lCflYyMDI20siHuVFcMz5MBj5vm_cidlb4fmQWircZDV3Xamo5AbNOXHdCSzHo5N1n7r5FYrsHcZeUJ9Vhg1WWaEVb2TmJOzcGCmqhI14jymIMRdQBeg%3D%3D%22%5D%5D; gfg_pp=1281985||post; __gads=ID=1f354412156f3bf5:T=1774652566:RT=1777974285:S=ALNI_MYYr6DiKljKFg-UITpRWt9NjosNOA; __gpi=UID=000013952b7301be:T=1774652566:RT=1777974285:S=ALNI_MbzxfE0Qak9f1G-5k6qH1R4vWu9WA; __eoi=ID=7b49d7edd45f1538:T=1774652566:RT=1777974285:S=AA-Afjag6wqAw_hQRU4Gtn6mpCfW; _ga_DWCCJLKX3X=GS2.1.s1777973709$o4$g1$t1777974420$j60$l0$h0",
        "priority": "u=0, i",
        "referer": "https://www.google.com/",
        "sec-ch-ua": "\"Google Chrome\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
    }