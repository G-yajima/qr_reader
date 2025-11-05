import cv2
import pytest
from unittest.mock import patch, MagicMock, PropertyMock

from src.qr_decoder import QrDecorder
from src.qr_recorder import QrRecorder

def test_QrRecorder_initilize():
    r = QrRecorder()
    
    assert type(r.records) is list

# tests/test_qr_recorder.py



def test_QrRecorder_with_QrDecoder_attribute():
    """QrDecoderの属性をモック化"""
    r = QrRecorder()
    
    with patch('src.qr_decoder.QrDecorder') as MockQrDecoder:
        # モックインスタンスを作成
        mock_decoder = MagicMock()
        
        # current_codes属性を設定
        mock_decoder.current_codes = {"4_315"}
        
        # QrDecoderのコンストラクタがモックインスタンスを返す
        MockQrDecoder.return_value = mock_decoder
        
        # 実際の使用方法
        from src.qr_decoder import QrDecorder
        decoder = QrDecorder(droidcam_url="http://dummy:4747/video")
        decoder.decode_droidcam(confirmation_threshold=5)
        results = decoder.current_codes
        
        r.add_decodes(results)
    
    assert "4_315" in r.records
    assert len(r.records) == 1





