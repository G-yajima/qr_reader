import cv2
import pytest


from src.qr_decoder import decode_qr_image, decode_qr_droidcam

def test_decode_qr_testimage_single_sample():
    """サンプルQRコードが正しく読めるかのテスト"""
    img = cv2.imread("tests/data/TestImage_4_315.JPG")
    number = decode_qr_image(img)
    assert number == "4_315"

def test_decode_qr_droidcam_single_sample(droidcam_url):
    """droidcam経由で読み込めるかをテスト"""
    expected_qr_code = "4_315"

    results = decode_qr_droidcam(droidcam_url)
    
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


def test_decode_qr_droidcam_multiple_samples_SDcard(droidcam_url):
    """droidcam経由で複数のQRコードを読み込めるかをテスト"""
    expected_qr_codes = ["2_32", "2_34", "2_36",
                         "2_31", "2_33", "2_35"]
    
    results = decode_qr_droidcam(droidcam_url)
    
    # リストが返ってくることを確認
    assert isinstance(results, list), "結果はリストであるべき"
    
    # 期待する数だけ検出されることを確認
    assert len(results) == len(expected_qr_codes), (
        f"期待: {len(expected_qr_codes)}個, 実際: {len(results)}個"
    )
    
    # すべての期待値が含まれることを確認（順序不問）
    for expected in expected_qr_codes:
        assert expected in results, (
            f"'{expected}'が検出結果に含まれていない。検出結果: {results}"
        )