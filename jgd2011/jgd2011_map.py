import cartopy.crs as ccrs
import contextily as cx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('Agg')  # WSL2用
matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'

def main():
    crs = ccrs.epsg(6677)  # 平面直角座標系9系 (JGD2011)

    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(1, 1, 1, projection=crs)

    xmin, xmax = -100000.0, 20000.0
    ymin, ymax = -100000.0, 20000.0

    xs = np.linspace(xmin, xmax, 6)
    ys = np.linspace(ymin, ymax, 6)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # ベースマップ
    cx.add_basemap(
        ax,
        crs=crs,
        zoom=10,
        source="https://cyberjapandata.gsi.go.jp/xyz/blank/{z}/{x}/{y}.png"
    )
    ax.hlines(ys, xmin, xmax, colors="gray", linestyles="--", linewidth=0.8)
    ax.vlines(xs, ymin, ymax, colors="gray", linestyles="--", linewidth=0.8)

    for y in ys:
        for x in xs:
            ax.plot(x, y, marker="o", markersize=7.5, color="orange")
            ax.text(x=x, y=y, s=f"({x:.0f}, {y:.0f})", fontsize=12, color="orange", ha="left", va="bottom")

    # レイアウト調整
    fig.tight_layout(pad=0.5)

    output_file = "jgd2011_map.png"
    fig.savefig(output_file, bbox_inches="tight", pad_inches=0.2, dpi=300)
    print(f"ofile: {output_file}")

if __name__ == "__main__":
    main()

