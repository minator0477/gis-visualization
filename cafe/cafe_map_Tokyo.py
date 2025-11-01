import cartopy.crs as ccrs
import contextily as cx
import matplotlib.pyplot as plt
import pyproj
from matplotlib.offsetbox import AnchoredText
import matplotlib
matplotlib.use('Agg') # wsl2上で実行する場合のおまじない
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os
import glob

mode = "honban"
# mode = "test"
# gis_data_path = "/work/data/gis/"
shops_name = ["doutor", "starbucks-coffee", "St-Marc", "Komeda"]

def main():
    # 日本語フォントの設定
    # plt.rcParams["font.family"] = "Meiryo"
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'

    crs = ccrs.epsg(6677)  # 平面直角座標系 9系(JGD2011)

    # 座標系に対応したオブジェクト
    fig = plt.figure(figsize=(16, 9))  # 実際の出力サイズは描画領域で決まるため、ここでは最大サイズとして指定。
    ax = fig.add_subplot(1, 1, 1, projection=crs)  # projectionへのcrsの指定により地理空間に投影

    # 描画領域の設定（東京駅周辺の座標を確認して入力）
    xmin, xmax = -20000.0, 5000.0
    ymin, ymax = -45000.0, -25000.0

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # 鉄道のプロット
    gdf_rail = read_shape("/work/data/gis/N02-24/Shift-JIS/N02-24_RailroadSection.shp").to_crs(crs)
    plot_rail(gdf_rail, ax)

    # カフェのプロット
    df_list = []
    for shop in shops_name:
        df = read_file(f"./{shop}_merged.csv")
        print(f"shop: {shop}")
        df["shop"] = shop
        df_list.append(df)
    merged_df = pd.concat(df_list, ignore_index=True)
    gdf = df2gdf(merged_df, crs)
    plot_cafe(gdf, ax, "shop")

    # ベースマップ(OpenStreetMap)の追加
    cx.add_basemap(ax, crs=crs, zoom=14, source="https://cyberjapandata.gsi.go.jp/xyz/blank/{z}/{x}/{y}.png")

    # プロットエリアの枠を非表示
    ax.set_axis_off()

    # プロットエリア以外の部分をなくし、地図部分のみをファイルに出力
    fig.tight_layout(pad=0)

    output_file = f"cafe_map_Tokyo.png"

    fig.savefig(output_file, bbox_inches="tight", pad_inches=0, dpi=400)
    print(f"ofile: {output_file}")


def plot_cafe(gdf, ax, column):
    # 対象地域の適当な座標系を設定

    # ポリゴン描画
    gdf.plot(
        ax = ax,
        markersize = 6,
        legend = True,
        cmap = "gist_rainbow",
        column = column,
    )


def plot_rail(gdf, ax):
    gdf.plot(ax = ax, color="black", linewidth=1.0, legend=False)



def read_file(filename: str):
    df = pd.read_csv(filename)
    return df

def read_shape(filename):
    return gpd.read_file(filename)


def df2gdf(df, crs):
    # shapelyのPoint型に変換
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    df = df.drop(["longitude", "latitude"], axis=1)

    # GeoDataFrameに変換
    gdf = gpd.GeoDataFrame(df, geometry=geometry,)
    gdf = gdf.set_crs("EPSG:4326")
    gdf = gdf.to_crs(crs)

    return gdf


if __name__ == "__main__":
    main()
