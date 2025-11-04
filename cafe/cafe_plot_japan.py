import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import cartopy
from shapely.geometry import Point
import geopandas as gpd

matplotlib.use('Agg')  # WSL2用

mode = "honban"
shops_name = ["doutor", "starbucks-coffee", "St-Marc", "Komeda"]

def main():
    output_file = "cafe_plot_4maps.png"

    # 2×2 の地図レイアウトを作成
    fig, axes = plt.subplots(
        2, 2,
        figsize=(12, 12),
        subplot_kw={'projection': ccrs.PlateCarree()}
    )

    # 各カフェチェーンをループ
    for ax, shop in zip(axes.flat, shops_name):
        # 地図のベース設定
        ax.set_extent([125.0, 150.0, 27.5, 47.5])
        ax.coastlines(resolution='10m')
        ax.add_feature(cartopy.feature.LAND, facecolor='gray')
        ax.add_feature(cartopy.feature.OCEAN, facecolor='lightblue')

        # データ読み込みとGeoDataFrame化
        df = read_file(f"./{shop}_merged.csv")
        gdf = df2gdf(df)

        # 各店舗をプロット
        gdf.plot(
            ax=ax,
            markersize=3,
            color="red",
            alpha=0.7,
            edgecolor="none",
            transform=ccrs.PlateCarree()
        )

        # タイトルを設定
        ax.set_title(shop, fontsize=14, fontweight="bold")

    # レイアウト調整・保存
    plt.tight_layout(pad=0.5)
    plt.savefig(output_file, dpi=300, bbox_inches="tight", pad_inches=0)
    print(f"ofile: {output_file}")


def read_file(filename: str):
    df = pd.read_csv(filename)
    return df


def df2gdf(df):
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    return gdf


if __name__ == "__main__":
    main()

