import cv2
import pytest
from unittest.mock import patch, MagicMock, PropertyMock

from src.qr_decoder import QrDecorder
from src.qr_recorder import QrRecorder

def test_QrRecorder_initilize():
    r = QrRecorder()
    
    assert type(r.records) is list

# tests/test_qr_recorder.py



def test_QrRecorder_with_single_code():
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

def test_QrRecorder_with_ignore_same_codes_for_multiple_times():
    """複数回スキャンして重複を排除"""
    r = QrRecorder()
    expected_qr_codes = {"4_315", "3_123"}  # setに変更
    
    with patch('src.qr_decoder.QrDecorder') as MockQrDecoder:
        mock_decoder = MagicMock()
        MockQrDecoder.return_value = mock_decoder
        
        from src.qr_decoder import QrDecorder
        decoder = QrDecorder(droidcam_url="http://dummy:4747/video")
        
        # 1回目: 1個検出
        mock_decoder.current_codes = {"4_315"}
        decoder.decode_droidcam(confirmation_threshold=5)
        r.add_decodes(decoder.current_codes)
        
        # 2回目: 2個検出（1個は重複）
        mock_decoder.current_codes = {"4_315", "3_123"}
        decoder.decode_droidcam(confirmation_threshold=5)
        r.add_decodes(decoder.current_codes)
    
    # 検証（よりシンプル）
    assert len(r.records) == 2
    assert set(r.records) == expected_qr_codes






