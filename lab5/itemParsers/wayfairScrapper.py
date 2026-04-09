from bs4 import BeautifulSoup
from lab5.itemParsers.shopScrapper import ShopScrapper


class WayfairItemScrapper(ShopScrapper):
    headers = {
        ":authority": "www.wayfair.com",
        ":method": "GET",
        ":path": "/kitchen-tabletop/pdp/keurig-k-elite-single-serve-k-cup-pod-coffee-maker-with-iced-coffee-setting-and-strength-control-lbld1008.html?piid=33032610",
        ":scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "uk-UA,uk;q=0.9,en-GB;q=0.8,en;q=0.7,ru-UA;q=0.6,ru;q=0.5,en-US;q=0.4",
        "cache-control": "max-age=0",
        "cookie": (
            "ExCSNUtId=23e0884a-6908-d0ce-b08f-48c027800a02; WFDC=DSM; CSNUtId=a1f5fda7-8ad2-4e81-919a-893114f603c8; "
            "_pxvid=1470d71e-33f4-11f1-8436-17f426c5ee0c; pxcts=1470dfe1-33f4-11f1-8436-b8a5fe2cc783; "
            "__pxvid=14d6e480-33f4-11f1-bcfd-665f42d769dc; postalCode=67346; i18nPrefs=lang%3Den-US; "
            "vid=90b4db30-7e22-4702-bc41-f0429d17d9df; SFSID=1124fe6b841f23801403215402a01da2; canary=0; "
            "serverUAInfo=%7B%22browser%22%3A%22Google%20Chrome%22%2C%22browserVersion%22%3A146%2C%22OS%22%3A%22Windows%22%2C%22OSVersion%22%3A%22%22%2C%22isMobile%22%3Afalse%2C%22isTablet%22%3Afalse%2C%22isTouch%22%3Afalse%7D; "
            "CSN_CSRF=5f0c2944b6ce61043607f3f5c4060fb0cb5012837c7b3cc1dbce8441e84494b9; _cnv_ses.f4d8=*; "
            "FVSID=49-6e1405bb-6810-483e-866e-e62e7c65df67; __ssid=677e43b0-4e91-48ce-a980-0c9bf3517de5; "
            "cjConsent=MHxOfDB8Tnww; cjUser=ff078c81-f91b-483f-86a4-5fd5206c177d; _twpid=tw.1775725886276.722346513950064397; "
            "_axwrt=42dc97f5-fdc0-4c30-a8bd-c26987d50929; __ps_r=https://www.google.com/; __ps_lu=https://www.wayfair.com/; "
            "__ps_did=pscrb_e59d6994-a986-4d8a-d3e2-ab50793c5dc8; __ps_fva=1775725886767; "
            "QuantumMetricSessionID=2216f96cd5427b7b85b14f85c909a7a4; QuantumMetricUserID=2ab3a5ec800f2151fc7e5bec8a59f040; "
            "_gcl_au=1.1.810726323.1775725887; IR_gbd=wayfair.com; _tt_enable_cookie=1; _ttp=01KNRR5G0VVFDHR2HKWT2P6A8M_.tt.1; "
            "g_state={\"i_l\":0,\"i_ll\":1775725887530,\"i_b\":\"NW733XzqP3Mr0uJVxdIgpnSdIQcGIEmn8trhfm/terw\",\"i_e\":{\"enable_itp_optimization\":0}}; "
            "_gid=GA1.2.50976044.1775725888; _zitok=df6ec29a3282b988dd661775725886; ndp_session_id=597a8f6d-4bc4-4942-af8b-cc0d07322ce2; "
            "fw_se={%22value%22:%22fws2.1dc002c0-9a49-4b77-a36c-7942acbd7360.1.1775725889695%22%2C%22createTime%22:%222026-04-09T09:11:29.695Z%22}; "
            "fw_uid={%22value%22:%228c484a7a-3b36-4da0-a820-fbb796ee2d0b%22%2C%22createTime%22:%222026-04-09T09:11:29.698Z%22}; "
            "fw_bid={%22value%22:%22oBWWO2%22%2C%22createTime%22:%222026-04-09T09:11:30.110Z%22}; "
            "fw_chid={%22value%22:%22xDzlrJJ%22%2C%22createTime%22:%222026-04-09T09:11:30.124Z%22}; hideGoogleYolo=true; "
            "_taggstar_vid=20e1173d-33f4-11f1-8597-7d33f436616d; axwrt=42dc97f5-fdc0-4c30-a8bd-c26987d50929; "
            "salsify_session_id=a1caee65-6539-4dba-9fc1-64635af1679c; _alby_user=37cfb077-9686-4868-8a92-88ca8b5241b6; pdp-views-count=5; "
            "_px2=eyJ1IjoiNzBkZGY0NjAtMzNmZS0xMWYxLWIyMjQtODc5ZTM3MTBiZTNhIiwidiI6IjE0NzBkNzFlLTMzZjQtMTFmMS04NDM2LTE3ZjQyNmM1ZWUwYyIsInQiOjE3NzU3MzA4MzQzMjIsImgiOiJjOGM1ZTk5YTlhYjlkZDY4Mzk1NjA2YWJjMjY0NGNjMjk2YjM3NjIwZGU4ZmQ2MmJmMzFjZTEwMzkyNTAwZGFlIn0=; "
            "Conviva_sdkConfig=%7B%22clId%22%3A%222082524633.1565166375.1944899360.1550449538%22%2C%22iid%22%3A1700313383%7D; "
            "datadome=OPg7SGLPkJT2AhviBFOWk~IChlxaP_2LOWF2kZ9lsNp6KpoL79DsWsyo53FoXhBs1ViwIGc06J0pGUiYBtH2H30kg5JC8_hp703UHx_l90K9Lg9zHKbEJU2WDkVNyNHG; "
            "_taggstar_ses=72bc32d6-33fe-11f1-b7df-4d60190e9159; __wid=947447728; _uetsid=16a1c27033f411f194e17d24a6058803; "
            "_uetvid=16a1e16033f411f189dbf1929f113d57; _ga_0GV7WXFNMT=GS2.1.s1775730338$o2$g1$t1775730338$j60$l0$h0; "
            "__ps_sr=_; __ps_slu=https://www.wayfair.com/kitchen-tabletop/pdp/keurig-k-elite-single-serve-k-cup-pod-coffee-maker-with-iced-coffee-setting-and-strength-control-lbld1008.html?piid=33032610; "
            "_rdt_uuid=1775725886829.bc852040-6b1e-4ea0-8dba-43188ac3ef33; _gat_gtag_UA_2081664_4=1; "
            "IR_12051=1775730338272%7C0%7C1775730338272%7C%7C; _ga_Q0HJWP456J=GS2.1.s1775730338$o2$g0$t1775730338$j60$l0$h0; "
            "_ga=GA1.1.1314230247.1775725887; ttcsid=1775730337687::kNpOHmg06t-oMBkjOdYJ.2.1775730338545.0::1.-5767.0::0.0.0.0::0.0.0; "
            "ttcsid_C7KTM4O68TKN71DEGAK0=1775730337686::HJmIfPRNrEeZjZgTBFdJ.2.1775730338545.0; "
            "forterToken=cc063b0bd8184d5bbcf60855ea2741a0_1775730336887__UDF43-m4_25ck_Cb1lC05Hl34%3D-5458-v2; "
            "forterToken=cc063b0bd8184d5bbcf60855ea2741a0_1775730336887__UDF43-m4_25ck_Cb1lC05Hl34%3D-5458-v2; "
            "_cnv_id.f4d8=5e079358-cec2-4c69-9e84-fba54ce67705.1775725885.1.1775730340..e21013f3-5fc7-41db-8c79-7200a288e89a...; "
            "CSNPersist=page_of_visit%3D24; "
            "ax_visitor=%7B%22firstVisitTs%22%3A1775725886761%2C%22lastVisitTs%22%3Anull%2C%22currentVisitStartTs%22%3A1775725886761%2C%22ts%22%3A1775730343189%2C%22visitCount%22%3A1%7D"
        ),
        "priority": "u=0, i",
        "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    }

    async def scrap_async(self, item_url: str) -> str | None:
        html = await self._load_html_by_url(item_url, headers=self.headers)
        if html is None:
            print(f'Failed to load HTML for url: {item_url}')
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        about_container = soup.find('div', attrs={'data-name': 'RomanceCopy'})
        features_container = soup.find('div', attrs={'data-name': 'FeatureBullets'})
        joined_text = about_container.text
        joined_text += features_container.text
        return joined_text
