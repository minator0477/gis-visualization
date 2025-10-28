import pandas as pd
import glob
import os

# CSVがあるディレクトリ（このスクリプトと同じ場所の場合は '.'）
input_dir = '.'
output_file = 'St-Marc_merged.csv'

# ディレクトリ内のすべてのCSVファイルを取得
csv_files = glob.glob(os.path.join(input_dir, '*.csv'))

# ファイルが見つからなかった場合の処理
if not csv_files:
    print("CSVファイルが見つかりません。")
else:
    # 全CSVを読み込み、1つのDataFrameに結合
    df_list = [pd.read_csv(f) for f in csv_files]
    merged_df = pd.concat(df_list, ignore_index=True)

    # 結合結果を出力
    merged_df.to_csv(output_file, index=False)
    print(f"{len(csv_files)} 個のCSVファイルを結合しました。出力: {output_file}")

