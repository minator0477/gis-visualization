import cartopy.crs as ccrs
import contextily as cx
import matplotlib.pyplot as plt
import pyproj
from matplotlib.offsetbox import AnchoredText
import matplotlib
matplotlib.use('Agg') # wsl2上で実行する場合のおまじない
import geopandas as gpd

mode = "honban"
# mode = "test"
gis_data_path = "/work/data/gis/"

"""
    項目一覧
        - A29_004: 用途地域分類コード
            - 1: 第一種低層住居専用地域
            - 2: 第二種低層住居専用地域
            - 3: 第一種中高層住居専用地域
            - 4: 第二種中高層住居専用地域
            - 5: 第一種住居地域
            - 6: 第二種住居地域
            - 7: 準住居地域
            - 8: 近隣商業地域
            - 9: 商業地域
            - 10: 準工業地域
            - 11: 工業地域
            - 12: 工業専用地域
            - 21: 田園住居地域
            - 99: 不明
"""

col_map = {
    "A29_004": "用途地域分類",
}

# 各列に対応する変換マップを定義
"""
mappings = {
    "A29_004": {
            1: "第一種低層住居専用地域",
            2: "第二種低層住居専用地域",
            3: "第一種中高層住居専用地域",
            4: "第二種中高層住居専用地域",
            5: "第一種住居地域",
            6: "第二種住居地域",
            7: "準住居地域",
            8: "近隣商業地域",
            9: "商業地域",
            10: "準工業地域",
            11: "工業地域",
            12: "工業専用地域",
            21: "田園住居地域",
            99: "不明",
     },
}
"""

mappings = {
    "A29_004": {
            1: "低層住居専用地域",
            2: "低層住居専用地域",
            3: "中高層住居専用地域",
            4: "中高層住居専用地域",
            5: "住居地域",
            6: "住居地域",
            7: "住居地域",
            8: "商業地域",
            9: "商業地域",
            10: "工業地域",
            11: "工業地域",
            12: "工業地域",
            21: "田園住居地域",
            99: "不明",
     },
}

def main():
    # 日本語フォントの設定
    # plt.rcParams["font.family"] = "Meiryo"
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'

    crs = ccrs.epsg(6677)  # 平面直角座標系 9系(JGD2011)

    # 座標系に対応したオブジェクト
    fig = plt.figure(figsize=(16, 9))  # 実際の出力サイズは描画領域で決まるため、ここでは最大サイズとして指定。
    ax = fig.add_subplot(1, 1, 1, projection=crs)  # projectionへのcrsの指定により地理空間に投影

    # 描画領域の設定（東京駅周辺の座標を確認して入力）
    xmin, xmax = -100000.0, 80000.0
    ymin, ymax = -90000.0, 60000.0

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    i = 9
    ifile = f"/work/data/gis/A29-11/A29-11_{i:02d}.shp"
    plot_shape(ifile, ax, True, crs)
    for i in [10, 11, 12, 13, 14]:
        ifile = f"/work/data/gis/A29-11/A29-11_{i:02d}.shp"
        plot_shape(ifile, ax, False, crs)

    # ベースマップ(OpenStreetMap)の追加
    cx.add_basemap(ax, crs=crs, zoom=12, source="https://cyberjapandata.gsi.go.jp/xyz/blank/{z}/{x}/{y}.png")


    # OpenStreetMapのクレジットを右下隅に表示
    # text_box = AnchoredText("© OpenStreetMap contributors", loc="lower right", borderpad=0, frameon=True)
    # plt.setp(text_box.patch, facecolor="white", alpha=0.6, linewidth=0)
    # ax.add_artist(text_box)

    # プロットエリアの枠を非表示
    ax.set_axis_off()

    # 凡例作成
    # ax.legend()

    # プロットエリア以外の部分をなくし、地図部分のみをファイルに出力
    fig.tight_layout(pad=0)

    if mode == "test":
        output_file = "output.png"
    else:
        output_file = f"用途地域分類_関東.png"

    fig.savefig(output_file, bbox_inches="tight", pad_inches=0, dpi=400)
    print(f"ofile: {output_file}")


def plot_shape(ifile, ax, need_legend, crs):
    # 対象地域の適当な座標系を設定

    gdf = gpd.read_file(ifile, encoding="cp932")

    # 各列に対応する辞書を適用
    for col, mapping in mappings.items():
        if col in gdf.columns:
            gdf[col] = gdf[col].map(mapping)

    # 列名変更
    gdf = gdf.rename(columns=col_map)

    # print(gdf["用途地域分類"])
    # 投影法の変換
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")

    gdf = gdf.to_crs("EPSG:6677")

    # ポリゴン描画
    gdf.plot(
        ax=ax, 
        column="用途地域分類",
        legend=need_legend,
        alpha=0.5,
        cmap="gist_rainbow",
        linewidth=0,
        edgecolor=None    
    )



def read_shape(filename: str):
    return gpd.read_file(filename)


if __name__ == "__main__":
    main()
