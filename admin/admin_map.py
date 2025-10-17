import cartopy.crs as ccrs
import contextily as cx
import matplotlib.pyplot as plt
import pyproj
from matplotlib.offsetbox import AnchoredText
import matplotlib
matplotlib.use('Agg') # wsl2上で実行する場合のおまじない

mode = "honban"
# mode = "test"
def main():
    # 日本語フォントの設定
    # plt.rcParams["font.family"] = "Meiryo"
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'

    # 対象地域の適当な座標系を設定
    crs = ccrs.epsg(6677)  # 平面直角座標系 9系(JGD2011)

    # 座標系に対応したオブジェクト
    fig = plt.figure(figsize=(16, 9))  # 実際の出力サイズは描画領域で決まるため、ここでは最大サイズとして指定。
    ax = fig.add_subplot(1, 1, 1, projection=crs)  # projectionへのcrsの指定により地理空間に投影

    # 描画領域の設定（東京駅周辺の座標を確認して入力）
    xmin, xmax = -80000.0, 6000.0
    ymin, ymax = -60000.0, -10000.0

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # ベースマップ(OpenStreetMap)の追加
    cx.add_basemap(ax, crs=crs, zoom=12, source="https://cyberjapandata.gsi.go.jp/xyz/blank/{z}/{x}/{y}.png")


    # OpenStreetMapのクレジットを右下隅に表示
    # text_box = AnchoredText("© OpenStreetMap contributors", loc="lower right", borderpad=0, frameon=True)
    # plt.setp(text_box.patch, facecolor="white", alpha=0.6, linewidth=0)
    # ax.add_artist(text_box)

    # プロットエリアの枠を非表示
    ax.set_axis_off()

    # プロットエリア以外の部分をなくし、地図部分のみをファイルに出力
    fig.tight_layout(pad=0)

    if mode == "test":
        output_file = "output.png"
    else:
        output_file = f"admin_map_{xmin:.0f}~{xmax:.0f}_{ymin:.0f}~{ymax:.0f}.png"

    fig.savefig(output_file, bbox_inches="tight", pad_inches=0, dpi=400)
    print(f"ofile: {output_file}")


if __name__ == "__main__":
    main()
