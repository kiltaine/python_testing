from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

wiki_url = "https://en.wikipedia.org/wiki/List_of_old-growth_forests"
wiki_data = urlopen(wiki_url)
wiki_html = wiki_data.read()
wiki_data.close()

page_soup = soup(wiki_html,'html.parser')
test_table = page_soup.find_all('table', class_='wikitable sortable')
test_table = test_table[0]
headers = test_table.find_all('th')
header_titles = []
for header in headers:
    header_titles.append(header.text[:-1])  # Remove trailing newline character
print(header_titles)

