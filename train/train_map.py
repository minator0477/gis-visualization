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

def main():
    # 日本語フォントの設定
    # plt.rcParams["font.family"] = "Meiryo"
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'

    # 対象地域の適当な座標系を設定
    crs = ccrs.epsg(6677)  # 平面直角座標系 9系(JGD2011)

    gdf_rail = read_shape(f"{gis_data_path}N02-24/Shift-JIS/N02-24_RailroadSection.shp").to_crs(epsg=6677)
    gdf_station = read_shape(f"{gis_data_path}N02-24/Shift-JIS/N02-24_Station.shp").to_crs(epsg=6677)


    # 座標系に対応したオブジェクト
    fig = plt.figure(figsize=(16, 9))  # 実際の出力サイズは描画領域で決まるため、ここでは最大サイズとして指定。
    ax = fig.add_subplot(1, 1, 1, projection=crs)  # projectionへのcrsの指定により地理空間に投影

    # 描画領域の設定（東京駅周辺の座標を確認して入力）
    xmin, xmax = -20000.0, 5000.0
    ymin, ymax = -45000.0, -25000.0

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # ベースマップ(OpenStreetMap)の追加
    cx.add_basemap(ax, crs=crs, zoom=12, source="https://cyberjapandata.gsi.go.jp/xyz/blank/{z}/{x}/{y}.png")

    gdf_rail[gdf_rail["N02_002"] == "1"].plot(ax = ax, color="red", alpha=0.75, linewidth=3.0, label="新幹線")
    gdf_rail[gdf_rail["N02_002"] == "2"].plot(ax = ax, color="orange", alpha=0.75, label="JR")
    gdf_rail[gdf_rail["N02_002"] == "3"].plot(ax = ax, color="green", alpha=0.75, label="公営鉄道")
    gdf_rail[gdf_rail["N02_002"] == "4"].plot(ax = ax, color="blue", alpha=0.75, label="私鉄")
    gdf_rail[gdf_rail["N02_002"] == "5"].plot(ax = ax, color="purple", alpha=0.75, label="第3セクター")
    gdf_station.plot(ax = ax, color="black", linewidth=2.5)
    # gdf_rail.plot(ax = ax, color="orange", label="1")

    # OpenStreetMapのクレジットを右下隅に表示
    # text_box = AnchoredText("© OpenStreetMap contributors", loc="lower right", borderpad=0, frameon=True)
    # plt.setp(text_box.patch, facecolor="white", alpha=0.6, linewidth=0)
    # ax.add_artist(text_box)

    # プロットエリアの枠を非表示
    ax.set_axis_off()

    # 凡例作成
    ax.legend()

    # プロットエリア以外の部分をなくし、地図部分のみをファイルに出力
    fig.tight_layout(pad=0)

    if mode == "test":
        output_file = "output.png"
    else:
        output_file = f"train_map_{xmin:.0f}~{xmax:.0f}_{ymin:.0f}~{ymax:.0f}.png"

    fig.savefig(output_file, bbox_inches="tight", pad_inches=0, dpi=400)
    print(f"ofile: {output_file}")


def read_shape(filename: str):
    return gpd.read_file(filename)


if __name__ == "__main__":
    main()
