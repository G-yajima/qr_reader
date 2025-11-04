import cv2

def test_camera_connection(droidcam_url):
    cap = cv2.VideoCapture()
    success = cap.open(droidcam_url)
    assert success, f"接続できませんでした💦 URL: {droidcam_url}"
    cap.release()