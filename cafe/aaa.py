import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import matplotlib
import pandas as pd
import cartopy
matplotlib.use('Agg') # wsl2上で実行する場合のおまじない
from shapely.geometry import Point
import geopandas as gpd

mode = "honban"
# mode = "test"
shops_name = ["doutor", "starbucks-coffee", "St-Marc", "Komeda"]

def main():
    output_file = "cafe_plot_japan.png"

    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([125.0, 150.0, 27.5, 47.5])
    ax.coastlines(resolution='10m')
    ax.add_feature(cartopy.feature.LAND, facecolor='gray')
    # ax.add_feature(cartopy.feature.OCEAN, facecolor='lightblue')

    # カフェのプロット
    df_list = []
    for shop in shops_name:
        df = read_file(f"./{shop}_merged.csv")
        print(f"shop: {shop}")
        df["shop"] = shop
        df_list.append(df)
    merged_df = pd.concat(df_list, ignore_index=True)
    gdf = df2gdf(merged_df)
    plot_cafe(gdf, ax, "shop")
    # ax.scatter(df["longitude"], df["latitude"], color="red", s=7.5, transform=ccrs.PlateCarree())
    fig.tight_layout(pad=0)
    plt.savefig(output_file, dpi=300, pad_inches=0)
    print(f"ofile: {output_file}")


def plot_cafe(gdf, ax, column):
    # 対象地域の適当な座標系を設定

    # ポリゴン描画
    gdf.plot(
        ax = ax,
        markersize = 2,
        legend = True,
        cmap = "gist_rainbow",
        column = column,
        linewidth = 0.15,
        edgecolor = "black",
    )


def read_file(filename: str):
    df = pd.read_csv(filename)
    return df



def df2gdf(df):
    # shapelyのPoint型に変換
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    df = df.drop(["longitude", "latitude"], axis=1)

    # GeoDataFrameに変換
    gdf = gpd.GeoDataFrame(df, geometry=geometry,)
    gdf = gdf.set_crs("EPSG:4326")
    # gdf = gdf.to_crs(crs)

    return gdf

if __name__ == "__main__":
    main()
