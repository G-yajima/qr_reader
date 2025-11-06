import cv2
import pytest
import time

from src.qr_decoder import QrDecorder, decode_qr_image
from src.qr_recorder import QrRecorder

def test_decode_qr_testimage_single_sample():
    """サンプルQRコードが正しく読めるかのテスト"""
    img = cv2.imread("tests/data/TestImage_4_315.JPG")
    number = decode_qr_image(img)
    assert number == "4_315"

@pytest.mark.integration
def test_decode_qr_droidcam_single_sample(droidcam_url):
    """droidcam経由で読み込めるかをテスト"""
    expected_qr_code = "4_315"

    r = QrRecorder()
    d = QrDecorder(droidcam_url)

    while True:
        try:
            d.decode_droidcam()
            results = list(d.current_codes)
            if d.state == "stop":
                break
        except ConnectionError as e:
            # print(f"⚠ 接続エラー: {e}")
            # print("  再接続を試みます...")
            time.sleep(2)
        
        except Exception as e:
            # print(f"⚠ エラー: {e}")
            time.sleep(1)
    
    # リストが返ってくることを確認
    assert isinstance(results, list), "結果はリストであるべき"
    
    # 1つだけ検出されることを確認
    assert len(results) == 1, (
        f"1つのQRコードが期待されるが、{len(results)}個検出された。"
        f"検出結果: {results}"
    )
    
    # 期待値と一致することを確認
    assert results[0] == expected_qr_code, (
        f"期待値: '4_315', 実際: '{results[0]}'"
    )