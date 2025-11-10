# conftest.py
def pytest_addoption(parser):
    parser.addoption(
        "--droidcam_url",
        action="store",
        default="http://192.168.0.114:4747/video",
        help="DroidCam の URL を指定（例: http://192.168.0.xxx:4747/video）",
    )

import pytest

@pytest.fixture
def droidcam_url(request):
    return request.config.getoption("--droidcam_url")

@pytest.fixture
def required_cols():
    return ["Label", "Location", "User"]


def pytest_runtest_logstart(nodeid, location):
    """テスト名が表示された直後に呼ばれる"""
    
    # テスト名に応じてメッセージを表示
    test_messages = {
        "test_decode_qr_droidcam_single_sample": ">>> 4_315のSDカードを読み取って",
        "test_QrRecorder_add_decode_multiple_codes": ">>> 1回目: 4_315のSDカード 2回目: 4_315と2のやつらを読み取って",
        "test_rewrite_file_test1_with_NoListed_label_with_doroidcam": ">> 2_25 2_26 4_288を読み取って",
    }
    
    # テスト名を取得
    test_name = nodeid.split("::")[-1]
    
    if test_name in test_messages:
        print(f"\n{test_messages[test_name]}", flush=True)