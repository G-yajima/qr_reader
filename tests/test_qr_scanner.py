import cv2
import pytest
from unittest.mock import patch

from src.qr_scanner import qr_scan

@pytest.mark.integration
def test_QrRecorder_add_decode_multiple_codes(droidcam_url):
    expected_qr_codes = ["2_32", "2_34", "2_36",
                         "2_31", "2_33", "2_35", "4_315"]
    r = qr_scan(droidcam_url)

    # 期待する数だけ検出されることを確認
    assert len(r.records) == len(expected_qr_codes), (
        f"期待: {len(expected_qr_codes)}個, 実際: {len(r.records)}個"
    )
    
    # すべての期待値が含まれることを確認（順序不問）
    for expected in expected_qr_codes:
        assert expected in r.records, (
            f"'{expected}'が検出結果に含まれていない。検出結果: {r.records}"
        )