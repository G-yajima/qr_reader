pytest -v --droidcam_url="http://192.168.0.114:4747/video"
みたいな感じでdroidocamのポートを指定。

読み取りテストを無視する場合
pytest -v --ignore=tests/test_qr_decoder.py --droidcam_url="http://192.168.0.180:4747/video"