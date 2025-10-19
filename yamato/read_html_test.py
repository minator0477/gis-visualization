from bs4 import BeautifulSoup
from address_to_latlon import call_gsi_api
import pandas as pd

# 1. ローカルに保存した index.html を開く
with open("kimono_yamato_shop.html", "r", encoding="utf-8") as f:
    html = f.read()

# 2. BeautifulSoup で解析
soup = BeautifulSoup(html, "html.parser")

address_arr = []
lats = []
lons = []

shop_elements = soup.find_all('div', class_="shopArticle__info")
for index, element in enumerate(shop_elements[:-1]):
#for index, element in enumerate(shop_elements[:2]):

    print(index)

    text = element.find_all('span')[1].string
    address = text.split()[0]
    address_arr.append(address)
    latitude, longitude = call_gsi_api(address)
    lats.append(latitude)
    lons.append(longitude)
    # print(index, address, latitude, longitude)

df = pd.DataFrame()
df["address"] = address_arr
df["latitude"] = lats
df["longitude"] = lons

df.to_csv("address.csv", index=False)
