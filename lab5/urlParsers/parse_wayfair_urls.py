from bs4 import BeautifulSoup
import csv

html_files = [
    r'lab5/offtop/Coffee Maker Keurig _ Wayfair.html',
    r'lab5/offtop/Coffee Maker Keurig _ Wayfair2.html',
    r'lab5/offtop/Coffee Maker Keurig _ Wayfair3.html'
]
output_file = r'lab5/offtop/wayfair_urls.csv'

urls = []

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')

    # Wayfair PDP links often contain /pdp/ and end with .html
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/pdp/' in href and '.html' in href:
            if href.startswith('/'):
                href = 'https://www.wayfair.com' + href
            
            if '?' in href:
                href = href.split('?')[0]
            
            if href not in urls:
                urls.append(href)

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['url'])
    for url in urls:
        writer.writerow([url])
