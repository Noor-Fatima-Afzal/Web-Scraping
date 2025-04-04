import requests
from bs4 import BeautifulSoup
import pandas as pd

books = []
for i in range(1,51):
    url = f"https://books.toscrape.com/catalogue/page-{i}.html"

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "lxml")

    ol = soup.find('ol')

    articles = ol.find_all('article', class_ = 'product_pod')

    for article in articles:
        image = article.find('img')
        titles = image.attrs['alt']
        star = article.find('p')
        star = star['class'][1]
        price = article.find('p', class_ = 'price_color').text
        price = price[1:]
        books.append([titles, price, star])

df = pd.DataFrame(books, columns=['Title','Price','Star Rating'])

df.to_csv('books.csv')