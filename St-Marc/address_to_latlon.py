import requests
import time
import urllib.parse



def main():
    address_list = ["東京都大田区北嶺町", "東京都大田区東嶺町"]
    for address in address_list:
        result = call_gsi_api(address)
        print(f"{address}: {result}")
        time.sleep(1.25)


class NoResultError(Exception):
    """APIのレスポンスが空だった場合に発生する例外"""
    pass


def call_gsi_api(address: str):
    """
    住所を緯度経度に変換する。見つからないときは(None, None)を返す
    (lat, lon) を返す
    """
    query =  urllib.parse.quote(address) # URLエンコード
    url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={query}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() # HTTPステータスコードが200番台（成功）でないときに例外を発生させる

    except:
        print(f"リクエスト失敗: {address} -> {e}")
        return None, None

    data = response.json()
    if not data:
        # print(f"結果なし: {address}")
        raise NoResultError(f"結果なし: {address}")

    first = data[0]
    coords = first.get("geometry", {}).get("coordinates")
    if coords and len(coords)  >= 2:
        lon, lat = coords[0], coords[1]
        return lat, lon
        
    else:
        print(f"座標取得失敗: {address} -> {first}")
        return None, None

if __name__ == "__main__":
    main()
