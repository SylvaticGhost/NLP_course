from bs4 import BeautifulSoup
import csv
import os

html_file = r'lab5/offtop/Coffee Maker Keurig for sale _ eBay_p1.html'
output_file = r'lab5/offtop/ebay_urls.csv'

with open(html_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')

urls = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if 'www.ebay.com/itm/' in href:
        if '?' in href:
            href = href.split('?')[0]
        if href not in urls:
            urls.append(href)

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['url'])
    for url in urls:
        writer.writerow([url])

