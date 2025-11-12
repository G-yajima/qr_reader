# excel関連
import pandas as pd
import warnings
import os
import time

# フォーマットチェック
from src.format_excel import format_excel

def rewrite_excel(path_excel, required_cols, save_log_dir, qr_labels, to_Location, to_User, to_Date):
    current_excel = pd.read_excel(path_excel)
    format_excel(current_excel, required_cols)

    # 文字列に変換しておく
    current_excel["Label"] = current_excel["Label"].astype(str)

    # 時刻の準備
    local_time = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d-%H-%M-%S", local_time)

    # ⚠️ 未記載ラベルチェック
    no_listed_labels = [label for label in qr_labels if label not in current_excel["Label"].values]
    warning_message = None  # ← 警告を一時的に保持

    if len(no_listed_labels) != 0:
        no_listed_labels_df = pd.DataFrame({"label": no_listed_labels})
        save_path = os.path.join(save_log_dir, formatted_time + "_No_listed_qrcodes.xlsx")
        no_listed_labels_df.to_excel(save_path, index=False)
        warning_message = f"以下のラベルはExcelにありません: {no_listed_labels}\nログ: {save_path}"

    # ✏️ Excel更新処理
    mask = current_excel["Label"].isin(qr_labels)
    current_excel.loc[mask, "Location"] = to_Location
    current_excel.loc[mask, "User"] = to_User
    # 列全体をdatetimeに変換してから代入する
    current_excel.loc[mask, "UpdateDate"] = to_Date

    current_excel.to_excel(path_excel, index=False)

    # 🧾 検出ラベルログ
    listed_labels = [label for label in qr_labels if label in current_excel["Label"].values]
    scaned_df = pd.DataFrame({"label": listed_labels})
    save_path = os.path.join(save_log_dir, formatted_time + "_scanned_qrcodes.xlsx")
    scaned_df.to_excel(save_path, index=False)

    # 最後に警告メッセージを返す（なければNone）
    return warning_message
