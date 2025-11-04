import cartopy.crs as ccrs
import contextily as cx
import matplotlib.pyplot as plt
import pyproj
import matplotlib
matplotlib.use('Agg')  # wsl2上で実行する場合のおまじない
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import cartopy

# カフェリスト
shops_name = ["doutor", "starbucks-coffee", "St-Marc", "Komeda"]

def main():
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'

    # 投影法（JGD2011 平面直角座標9系）
    crs = ccrs.epsg(6677)

    # 描画範囲（東京駅周辺）
    xmin, xmax = -20000.0, 5000.0
    ymin, ymax = -45000.0, -25000.0

    # 図と4つのサブプロット作成（2x2配置）
    fig, axes = plt.subplots(
        2, 2,
        figsize=(14, 10),
        subplot_kw={'projection': crs}
    )

    # 鉄道データを事前読み込み
    gdf_rail = read_shape("/work/data/gis/N02-24/Shift-JIS/N02-24_RailroadSection.shp").to_crs(crs)

    # 行政界データを事前読み込み
    land = gpd.read_file("/work/data/gis/N03-140401/N03-140401_GML/N03-14_140401.shp").to_crs(crs)

    for ax, shop in zip(axes.flatten(), shops_name):
        # データ読み込み
        print(f"shop: {shop}")
        df = read_file(f"./{shop}_merged.csv")
        df["shop"] = shop
        gdf = df2gdf(df, crs)

        # 行政界
        land.plot(ax=ax, color="lightgray", linewidth=0.25, edgecolor="dimgray")


        # 鉄道とカフェを描画
        plot_rail(gdf_rail, ax)
        plot_cafe(gdf, ax, "shop")

        # 軸・枠の設定
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.set_axis_off()

        # タイトル
        ax.set_title(shop, fontsize=14)

    # レイアウト調整と保存
    fig.tight_layout(pad=0)
    output_file = "cafe_plot_Tokyo_4subplots.png"
    fig.savefig(output_file, bbox_inches="tight", pad_inches=0, dpi=400)
    print(f"ofile: {output_file}")


def plot_cafe(gdf, ax, column):
    gdf.plot(
        ax=ax,
        markersize=6,
        legend=False,
        cmap="gist_rainbow",
        column=column,
    )

def plot_rail(gdf, ax):
    gdf.plot(ax=ax, color="black", linewidth=1.0, legend=False)

def read_file(filename: str):
    return pd.read_csv(filename)

def read_shape(filename):
    return gpd.read_file(filename)

def df2gdf(df, crs):
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    df = df.drop(["longitude", "latitude"], axis=1)
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    return gdf.to_crs(crs)


if __name__ == "__main__":
    main()

