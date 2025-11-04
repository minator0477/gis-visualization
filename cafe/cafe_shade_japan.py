import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import cartopy
from shapely.geometry import Point
import geopandas as gpd
import numpy as np
from matplotlib.colors import LogNorm
matplotlib.use('Agg')  # WSL2用

mode = "honban"
shops_name = ["doutor", "starbucks-coffee", "St-Marc", "Komeda"]
matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'

def main():

    # 2×2 の地図レイアウトを作成
    fig, axes = plt.subplots(
        2, 2,
        figsize=(12, 12),
        subplot_kw={'projection': ccrs.PlateCarree()}
    )
    gdf_admin = read_shape("/work/data/gis/N03-140401/N03-140401_GML/N03-14_140401.shp")
    area = calculate_area(gdf_admin)
    gdf_admin['area'] = area

    gdf_list = []
    max_list = []
    for shop in shops_name:
        print(f'shop: {shop}')
        gdf_tmp = gdf_admin.copy()

        # データ読み込みとGeoDataFrame化
        df_cafe = read_file(f"./{shop}_merged.csv")
        gdf_cafe = df2gdf(df_cafe)

        counts = count(gdf_cafe, gdf_tmp)
        gdf_tmp['count'] = counts
        gdf_tmp['area'] = area
        gdf_tmp['density'] = counts / area
        gdf_list.append(gdf_tmp)
        max_list.append(gdf_tmp['density'].values.max())

    vmin = 1e-6
    vmax = max(max_list)
    norm = LogNorm(vmin=vmin, vmax=vmax)

    # 各カフェチェーンをループ
    for ax, shop, gdf in zip(axes.flat, shops_name, gdf_list):
        print(f'shop: {shop}')
        # 地図のベース設定
        ax.set_extent([125.0, 150.0, 27.5, 47.5])
        ax.coastlines(resolution='10m')
        # ax.add_feature(cartopy.feature.LAND, facecolor='gray')
        # ax.add_feature(cartopy.feature.OCEAN, facecolor='lightblue')

        gdf.loc[gdf['density'] == 0, 'density'] = np.nan
        gdf.plot(
            ax = ax,
            column = 'density',
            legend = True,
            cmap = "Oranges",
            norm = norm,
            legend_kwds = {'shrink': 0.6, 'label': '店舗密度 [#/km^2]'}
        )

        # タイトルを設定
        ax.set_title(shop, fontsize=14, fontweight="bold")

    output_file = "cafe_shade_japan_4maps.png"
    # レイアウト調整・保存
    plt.tight_layout(pad=0.5)
    plt.savefig(output_file, dpi=300, bbox_inches="tight", pad_inches=0)
    print(f"ofile: {output_file}")


def read_file(filename: str):
    df = pd.read_csv(filename)
    return df


def read_shape(filename: str):
    gdf = gpd.read_file(filename)
    return gdf


def df2gdf(df):
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    return gdf


def calculate_area(gdf):
    g = gdf.copy()
    g.crs = "epsg:4612"
    g = g.to_crs(epsg = 3099)
    area = g['geometry'].area / 1000000.
    return area


def count(gdf, gdf_admin):
    # for i in range(len(gdf):
    # for i in range(len(gdf[:1])):
    mask = np.asarray([gdf_admin.contains(g).values for g in gdf['geometry']])
    counts = mask.sum(axis=0)
    
    #####################
    # mask配列
    # ---,      市町村1,  市町村2,  ・・・, 市町村n
    # 店舗1, False,   True,・・・, False
    # 店舗2
    # ・・・
    # 店舗n


    #####################
    return counts    


if __name__ == "__main__":
    main()

