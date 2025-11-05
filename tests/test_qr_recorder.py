import cv2
import pytest
from unittest.mock import patch



from src.qr_decoder import decode_qr_image, decode_qr_droidcam
from src.qr_recorder import QrRecorder
from src.qr_scanner import qr_scan

def test_QrRecorder_initilize():
    r = QrRecorder()
    
    assert type(r.recods) is list

def test_QrRecorder_add_decode_with_mock():
    r = QrRecorder()
    
    with patch('src.qr_decoder.decode_qr_droidcam') as mock_decode:
        mock_decode.return_value = ["4_315"]
        
        # ✅ モックを直接呼ぶ（インポート不要）
        results = mock_decode("http://dummy:4747/video")
        r.add_decodes(results)
    
    assert "4_315" in r.recods





