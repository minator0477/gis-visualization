from bs4 import BeautifulSoup
from address_to_latlon import call_gsi_api, NoResultError
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
for i in range(25):
# for i in range(1):

    with open(f"Komeda_{i:02d}.html", "r", encoding="utf-8") as f:
        html = f.read()

# 2. BeautifulSoup で解析
    soup = BeautifulSoup(html, "html.parser")

    names = []
    address_arr = []
    lats = []
    lons = []

    shops = soup.find_all("li", class_="shop__item")
    print("count:", len(shops))
    for shop in shops:
        # print(shop)
        shop_name = shop.find('h3', class_="shop-casset__ttl").get_text(strip=True).split()[-1]
        shop_address = shop.find('p', class_="shop-casset__address").get_text(strip=True).split()[0]
        print(f"name: {shop_name}, address: {shop_address}")
        names.append(shop_name)
        address_arr.append(shop_address)
        try:
            lat, lon = call_gsi_api(shop_address)
            lats.append(lat)
            lons.append(lon)
        except NoResultError as e:
            print("想定していた例外をキャッチ:", e)
            lats.append(None)
            lons.append(None)
        # , shop_address)

    df = pd.DataFrame()
    df["name"] = names
    df["address"] = address_arr
    df["latitude"] = lats
    df["longitude"] = lons

    ofile = f"Komeda_{i:02d}.csv"
    df.to_csv(ofile, index=False, na_rep="NaN")
    print(f"ofile: {ofile}")
