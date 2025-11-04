import cv2
from src.qr_decoder import decode_qr

def test_decode_qr_sample():
    """サンプルQRコードが正しく読めるかのテスト"""
    img = cv2.imread("tests/data/TestImage_4_315.JPG")
    result = decode_qr(img)
    assert result == "4_315"