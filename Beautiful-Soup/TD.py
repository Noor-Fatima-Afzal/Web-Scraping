import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://ticker.finology.in/'
r = requests.get(url)
# print(r) 

soup = BeautifulSoup(r.text, 'lxml')

table = soup.find('table', class_= "table table-sm table-hover screenertable")
header = table.find_all('th')
# print(header)

titles = []
for i in header:
    title = i.text.strip()
    titles.append(title)

df = pd.DataFrame(columns=titles)

rows = table.find_all('tr')

for i in rows[1:]:
    data = i.find_all('td')
    row = [tr.text.strip() for tr in data]
    l = len(df)
    df.loc[l] = row

print(df)