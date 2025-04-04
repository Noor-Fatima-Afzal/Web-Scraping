import requests
from bs4 import BeautifulSoup
import pandas as pd

r = requests.get("https://www.iplt20.com/auction/2022")

soup = BeautifulSoup(r.text, "lxml")

# print(soup.prettify())  

table = soup.find("table", class_="ih-td-tab auction-tbl")

headers = []
for th in table.find_all("th"):
    headers.append(th.text.strip())

df = pd.DataFrame(columns=headers)

rows = table.find_all("tr")

for i in rows[1:]:
    data = i.find_all("td")
    row_data = [td.text.strip() for td in data]
    l = len(df)
    df.loc[l] = row_data

print(df)

df.to_csv("ipl_auction.csv", index=False)