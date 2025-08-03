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

all_rows = test_table.find_all('tr')
data = all_rows[1:]


first_row = data[0]
first_row_data = first_row.find_all('td')


data_texts = []
for data_text in first_row_data:
    data_texts.append(data_text.text[:-1])

table_rows = []
for row in data:
    table_row = []
    row_data = row.find_all('td')
    for data_point in row_data:
        table_row.append(data_point.text[:-1])
    table_rows.append(table_row)


filename = 'test_table.csv'
f = open(filename, 'w', encoding='utf-8')
header_string = ''
for title in header_titles:
    header_string += title + ','
header_string = header_string[:-1]
header_string+= '\n'


f.write(header_string)


for row in table_rows:
    row_string = ''
    for column in row:
        column_string = columnre
        row_string += column + ','
    row_string = row_string[:-1]     
    row_string += '\n'
    f.write(row_string)