import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import matplotlib
import pandas as pd
import cartopy
matplotlib.use('Agg') # wsl2上で実行する場合のおまじない

mode = "honban"
# mode = "test"
def main():
    input_file = "address.csv"
    output_file = "yamato_map.png"
    df = pd.read_csv(input_file)
    #print(df)

    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([125.0, 150.0, 27.5, 47.5])
    ax.coastlines(resolution='10m')
    ax.add_feature(cartopy.feature.LAND, facecolor='lightgreen')
    ax.add_feature(cartopy.feature.OCEAN, facecolor='lightblue')

    ax.scatter(df["longitude"], df["latitude"], color="red", s=7.5, transform=ccrs.PlateCarree())

    plt.savefig(output_file, dpi=200)
    print(f"ofile: {output_file}")

if __name__ == "__main__":
    main()
