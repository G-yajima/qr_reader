# excel関連
import pandas as pd
import warnings
import os

def rewrite_excel(path_excel, save_dir, qr_labels, to_Location, to_User):
    # Excelの読み込み
    current_excel = pd.read_excel(path_excel)

    # 未記載ラベルの検出と警告
    no_listed_labels = [label for label in qr_labels if label not in current_excel["Label"].values]
    if len(no_listed_labels) != 0:
        warnings.warn(f"以下のラベルはExcelにありません: {no_listed_labels}")
        no_listed_labels_df = pd.DataFrame({"label": no_listed_labels})
        save_path = os.path.join(save_dir, "No_listed_qrcodes.xlsx")
        no_listed_labels_df.to_excel(save_path, index=False)
    
    # 該当SDの情報を書き換える
    mask = current_excel["Label"].isin(qr_labels)
    current_excel.loc[mask, "Location"] = to_Location
    current_excel.loc[mask, "User"] = to_User

    # 保存: 本体
    save_path = os.path.join(save_dir, "rewrite_file.xlsx")
    current_excel.to_excel(save_path, index=False)

    # 保存: 検出ラベル
    scaned_df = pd.DataFrame({"label": qr_labels})
    save_path = os.path.join(save_dir, "scanned_qrcodes.xlsx")
    scaned_df.to_excel(save_path, index=False)