from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# ヘッドレスモード（ブラウザを表示せずに実行）
chrome_options = Options()
chrome_options.add_argument("--headless")

# Chromeドライバのパスを指定
service = Service('/usr/local/bin/chromedriver')

prefectures_kata = ["hokkaido", \
"aomori","iwate","miyagi","akita","yamagata","fukushima", \
"ibaraki","tochigi","gunma","saitama","chiba","tokyo","kanagawa", \
"niigata","toyama","ishikawa","fukui","yamanashi","nagano","gifu","shizuoka","aichi", \
"mie","shiga","kyoto","osaka","hyogo","nara","wakayama", \
"tottori","shimane","okayama","hiroshima","yamaguchi", \
"tokushima","kagawa","ehime","kochi", \
"fukuoka","saga","nagasaki","kumamoto","oita","miyazaki","kagoshima","okinawa"]

for prefecture in prefectures_kata:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print(prefecture)
    # ページを開く
    url = f"https://store.starbucks.co.jp/pref/{prefecture}/"

    driver.get(url)

    # ページ全体のbodyタグがレンダリングされるまで待機
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # ページ全体のHTMLを取得
    html_source = driver.page_source

    # HTMLをファイルに保存（後で解析可能）
    ofile = f"{prefecture}.html"
    with open(ofile, "w", encoding="utf-8") as f:
        f.write(html_source)

    driver.quit()
    print(f"HTMLを{ofile} に保存しました。")
