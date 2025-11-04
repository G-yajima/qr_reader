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
