import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg') # wsl2上で実行する場合のおまじない
import pandas as pd

def main():
    clim, std = read()
    # print(clim, std)
    theta = 2 * np.pi * np.arange(len(clim)) / len(clim) # 365日分のtheta
    theta = np.concatenate((theta, [theta[0]]))  # 閉じた多角形にする
    clim = np.concatenate((clim, [clim[0]]))
    std = np.concatenate((std, [std[0]]))


    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)

    # データプロット
    ax.plot(theta, clim, label="clim")  # 気候値（線）
    ax.fill_between(theta, clim - std, clim + std, color="blue", alpha=0.2, label="±1σ") # 標準偏差
    plt.legend()


    # Nを0度に
    ax.set_theta_zero_location('N')  # 'N', 'E', 'S', 'W'（北・東・南・西）
    months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
    angles_month = 360. * np.arange(12) / 12.
    ax.set_thetagrids(angles_month, months)  # 軸ラベル
    ax.set_rgrids([0, 10, 20, 30], labels=None, angle=30, fmt=None) # 軸ラベル
    ax.set_theta_direction(-1) # 角度を時計回りに
    ax.set_rlim(0 ,35)
    ax.tick_params(labelsize=15)
    ax.set_title("Temperature [degC] @Tokyo", fontsize=20.)

    # 出力
    imgname = "temperature_Tokyo_amedas.png"
    fig.savefig(imgname)
    plt.close(fig)

def read():
    # climatelogy
    clim_file = "/work/data/meteorology/weather_Tokyo_amedas_clim.csv"
    df_clim = pd.read_csv(clim_file)
    df_clim = df_clim[df_clim["年月日"] != "02-29"]
    clim_data = df_clim["気温"].values

    # standard deviation
    std_file = "/work/data/meteorology/weather_Tokyo_amedas_std.csv"
    df_std = pd.read_csv(std_file)
    df_std = df_std[df_std["年月日"] != "02-29"]
    std_data = df_std["気温"].values

    return clim_data, std_data

if __name__ == "__main__":
    main()
