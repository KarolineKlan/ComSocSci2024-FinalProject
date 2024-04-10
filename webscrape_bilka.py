import requests
from bs4 import BeautifulSoup

LINK = "https://www.bilkatogo.dk/kategori/"
categories = ["frugt-og-groent/", "koed-og-fisk/", "mejeri-og-koel/"]


SCRAPE_LINK = LINK + categories[1]
LINK = "https://www.bilkatogo.dk/kategori/frugt-og-groent/"

r = requests.get(SCRAPE_LINK)  # Make a request to the website
soup = BeautifulSoup(r.content)
products = soup.find_all('div', {'class': 'row'})
r2 = products[0].find("div", {'data-v-da5161c2': True, 'data-v-e0535ac4': True})

print(1)