# excel関連
import pandas as pd
import warnings
import os
import time

# フォーマットチェック
from src.format_excel import format_excel

def rewrite_excel(path_excel, required_cols, save_log_dir, qr_labels, to_Location, to_User):
    # Excelの読み込み
    current_excel = pd.read_excel(path_excel)

    # 列のチェック
    format_excel(current_excel, required_cols)

    # 現在時刻の取得
    # 現在の時刻をフォーマットして表示
    local_time = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d-%H-%M-%S", local_time)

    # 未記載ラベルの検出と警告
    no_listed_labels = [label for label in qr_labels if label not in current_excel["Label"].values]
    if len(no_listed_labels) != 0:
        warnings.warn(f"以下のラベルはExcelにありません: {no_listed_labels}")
        no_listed_labels_df = pd.DataFrame({"label": no_listed_labels})
        save_path = os.path.join(save_log_dir, formatted_time + "_No_listed_qrcodes.xlsx")
        no_listed_labels_df.to_excel(save_path, index=False)
    
    # 記載ラベルの検出
    listed_labels = [label for label in qr_labels if label in current_excel["Label"].values]
    
    # 該当SDの情報を書き換える
    mask = current_excel["Label"].isin(qr_labels)
    current_excel.loc[mask, "Location"] = to_Location
    current_excel.loc[mask, "User"] = to_User

    # 保存: 本体
    current_excel.to_excel(path_excel, index=False)

    # 保存: 検出ラベル
    scaned_df = pd.DataFrame({"label": listed_labels})
    save_path = os.path.join(save_log_dir, formatted_time + "_scanned_qrcodes.xlsx")
    scaned_df.to_excel(save_path, index=False)