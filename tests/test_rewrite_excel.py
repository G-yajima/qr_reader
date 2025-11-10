# excel関連
import pandas as pd
from src.rewrite_excel import rewrite_excel

# ファイルの操作
import os
import shutil

# Test関連
import pytest
from unittest.mock import patch, MagicMock

# QR関連
from src.qr_scanner import qr_scan

def test_rewrite_file_test1_with_NoListed_label(tmp_path, required_cols):
    """
    最初の二行 (2_31と2_32) 
    1. Locationを「研究室」から「房総」へ
    2. Userを「矢島」から「松岡」へ
    3. UpdateDateを「1999/1/1」から「2025/11/3」へ
    4. エクセルには存在しない「1_996と8_712」が存在
    """
    # 変更したい項目
    to_Location   = "房総"
    to_User       = "松岡"
    to_Date       = 20251103
    path_excel    = tmp_path / "TestExcel.xlsx"
    # path_excel    = "C:/Users/fores/Downloads/TestExcel.xlsx"
    save_log_dir  = "tests/output"

    # 期待するエクセルファイル
    expected_excel = pd.read_excel("tests/data/TestExcel_test1_expected.xlsx")

    # qr_scanの出力
    with patch('src.qr_scanner.qr_scan') as mock_qr_scan:
        '''
        この中では qr_scan が偽物になっている
        from src.qr_scanner import qr_scan
        print(qr_scan is mock_qr_scan)  # Trueになるということ
        '''
        mock_recorder = MagicMock()
        mock_recorder.records = ["2_25", "2_26", "8_712", "1_996"]
        mock_qr_scan.return_value = mock_recorder
        
        from src.qr_scanner import qr_scan # この qr_scan は偽物
        r = qr_scan("http://dummy:4747/video")
        qr_labels = r.records
    '''ブロックを出ると元に戻る'''

    # 書き換えと保存
    ## ファイルの準備（複製）
    src_path = "tests/data/TestExcel_org.xlsx"
    shutil.copy(src_path, path_excel)

    # 評価1: warnings.warn の捕捉と検証
    warning_msg = rewrite_excel(path_excel, required_cols, save_log_dir, qr_labels, to_Location, to_User, to_Date)
    assert warning_msg is not None
    assert "以下のラベルはExcelにありません" in warning_msg

    rewrite_file = pd.read_excel(path_excel)
    # os.remove(path_excel)

    # 評価2: 出力ファイルの比較
    assert (rewrite_file["Location"] == expected_excel["Location"]).all()
    assert (rewrite_file["User"] == expected_excel["User"]).all()
    assert (rewrite_file["UpdateDate"] == expected_excel["UpdateDate"]).all()

@pytest.mark.integration
def test_rewrite_file_test1_with_NoListed_label_with_doroidcam(tmp_path, droidcam_url, required_cols):
    """
    droidcamバージョン
    含まれてる  : 2_25, 2_26
    含まれてない: 4_288
    """
    # 変更したい項目
    to_Location   = "房総"
    to_User       = "松岡"
    to_Date       = 20251103
    path_excel    = tmp_path / "TestExcel.xlsx"
    save_log_dir  = "tests/output"

    # 期待するエクセルファイル
    expected_excel = pd.read_excel("tests/data/TestExcel_test1_expected.xlsx")

    # qr_scanの出力
    r = qr_scan(droidcam_url)
    qr_labels = r.records

    # 書き換えと保存
    ## ファイルの準備（複製）
    src_path = "tests/data/TestExcel_org.xlsx"
    shutil.copy(src_path, path_excel)

    # 評価1: warnings.warn の捕捉と検証
    warning_msg = rewrite_excel(path_excel, required_cols, save_log_dir, qr_labels, to_Location, to_User, to_Date)
    assert warning_msg is not None
    assert "以下のラベルはExcelにありません" in warning_msg

    rewrite_file = pd.read_excel(path_excel)
    os.remove(path_excel)

    # 評価2: 出力ファイルの比較
    assert (rewrite_file["Location"] == expected_excel["Location"]).all()
    assert (rewrite_file["User"] == expected_excel["User"]).all()
    assert (rewrite_file["UpdateDate"] == expected_excel["UpdateDate"]).all()