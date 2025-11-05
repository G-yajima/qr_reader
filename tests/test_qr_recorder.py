import cv2
import pytest


from src.qr_decoder import decode_qr_image, decode_qr_droidcam
from src.qr_recorder import QrRecorder

def test_QrRecorder_initilize():
    r = QrRecorder()
    
    assert type(r.recodes) is list

def test_QrRecorder_add_decode(droidcam_url):
    r = QrRecorder()
    results = decode_qr_droidcam(droidcam_url)
    r.add_decodes(results)

    assert r.recodes[0] == "4_315"

def test_QrRecorder_add_decode_ignore_same_SD(droidcam_url):
    expected_qr_codes = ["2_32", "2_34", "2_36",
                         "2_31", "2_33", "2_35", "4_315"]
    r = QrRecorder()

    results = decode_qr_droidcam(droidcam_url)
    r.add_decodes(results)

    results = decode_qr_droidcam(droidcam_url)
    r.add_decodes(results)

    # 期待する数だけ検出されることを確認
    assert len(r.recodes) == len(expected_qr_codes), (
        f"期待: {len(expected_qr_codes)}個, 実際: {len(r.recodes)}個"
    )
    
    # すべての期待値が含まれることを確認（順序不問）
    for expected in expected_qr_codes:
        assert expected in r.recodes, (
            f"'{expected}'が検出結果に含まれていない。検出結果: {r.recodes}"
        )





