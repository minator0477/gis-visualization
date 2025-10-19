from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# ヘッドレスモード（ブラウザを表示せずに実行）
chrome_options = Options()
# chrome_options.add_argument("--headless")

# Chromeドライバのパスを指定
service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# ページを開く
driver.get("https://www.kimono-yamato.co.jp/shop/")

# ページ全体のbodyタグがレンダリングされるまで待機
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)

# ページ全体のHTMLを取得
html_source = driver.page_source

# HTMLをファイルに保存（後で解析可能）
with open("kimono_yamato_shop.html", "w", encoding="utf-8") as f:
    f.write(html_source)

print("HTMLを kimono_yamato_shop.html に保存しました。")

driver.quit()

