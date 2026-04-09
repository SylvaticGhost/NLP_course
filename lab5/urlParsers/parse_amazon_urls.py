from bs4 import BeautifulSoup
import csv
import os

html_files = [
    r'lab5/offtop/Amazon.com _ coffee machine keurig.html',
    r'lab5/offtop/Amazon.com_ Coffee Machine Keurig2.html',
    r'lab5/offtop/Amazon.com_ Coffee Machine Keurig3.html'
]
output_file = r'lab5/offtop/amazon_urls.csv'

urls = []

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')

    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/dp/' in href or '/gp/product/' in href:
            if href.startswith('/'):
                href = 'https://www.amazon.com' + href
            
            if '?' in href:
                href = href.split('?')[0]
            
            if '/ref=' in href:
                href = href.split('/ref=')[0]
            
            if href not in urls:
                urls.append(href)

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['url'])
    for url in urls:
        writer.writerow([url])
