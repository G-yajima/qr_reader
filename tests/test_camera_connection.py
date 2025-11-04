import cv2
import pytest
import threading

def test_camera_connection(droidcam_url):
    cap = cv2.VideoCapture()

    success = {"connected": False}

    def try_open():
        success["connected"] = cap.open(droidcam_url)

    t = threading.Thread(target=try_open, daemon=True)
    t.start()
    t.join(timeout=10)

    if t.is_alive() or not success["connected"]:
        cap.release()
        pytest.fail(f"カメラ({droidcam_url})に10秒以内に接続できませんでした...")

    ret, frame = cap.read()
    cap.release()

    assert ret, f"カメラは開けたけどフレームが取得できなかった..."