from bs4 import BeautifulSoup
from address_to_latlon import call_gsi_api
import pandas as pd

prefectures_kata = ["hokkaido", \
"aomori","iwate","miyagi","akita","yamagata","fukushima", \
"ibaraki","tochigi","gunma","saitama","chiba","tokyo","kanagawa", \
"niigata","toyama","ishikawa","fukui","yamanashi","nagano","gifu","shizuoka","aichi", \
"mie","shiga","kyoto","osaka","hyogo","nara","wakayama", \
"tottori","shimane","okayama","hiroshima","yamaguchi", \
"tokushima","kagawa","ehime","kochi", \
"fukuoka","saga","nagasaki","kumamoto","oita","miyazaki","kagoshima","okinawa"]
# 1. ローカルに保存した index.html を開く
for prefecture in prefectures_kata[:1]:

    with open(f"{prefecture}.html", "r", encoding="utf-8") as f:
        html = f.read()

# 2. BeautifulSoup で解析
    soup = BeautifulSoup(html, "html.parser")

    address_arr = []
    lats = []
    lons = []

    shop_elements = soup.find_all('div', class_="result__item__info")
    print(soup)
    """
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
    """
