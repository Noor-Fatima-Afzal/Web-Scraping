import requests
from bs4 import BeautifulSoup

url = "https://webscraper.io/test-sites/e-commerce/allinone/product/3"

r = requests.get(url)

soup = BeautifulSoup(r.text, "lxml")

# print(soup.prettify())

names = soup.find_all("h4", class_="title card-title")

for i in names:
    print(i.text)

prices = soup.find_all("h4", class_="price float-end pull-right")

for i in prices:
    print(i.text)