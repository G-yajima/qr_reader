import cv2
import pytest
from unittest.mock import patch



from src.qr_decoder import decode_qr_image, decode_qr_droidcam
from src.qr_recorder import QrRecorder
from src.qr_scanner import qr_scan


def test_QrRecorder_add_decode_ignore_same_SD(droidcam_url):
    expected_qr_codes = ["2_32", "2_34", "2_36",
                         "2_31", "2_33", "2_35", "4_315"]
    r = qr_scan(droidcam_url)

    # 期待する数だけ検出されることを確認
    assert len(r.recods) == len(expected_qr_codes), (
        f"期待: {len(expected_qr_codes)}個, 実際: {len(r.recods)}個"
    )
    
    # すべての期待値が含まれることを確認（順序不問）
    for expected in expected_qr_codes:
        assert expected in r.recods, (
            f"'{expected}'が検出結果に含まれていない。検出結果: {r.recods}"
        )