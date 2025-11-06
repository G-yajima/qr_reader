# QRを実際に読み込まないテストのみ
読み込みはモックしてる。
pytest -v -m "not integration"

# 統合テストのみ
pytest -v -m "integration" --droidcam_url="http://192.168.0.180:4747/video"

# すべて
pytest -v --droidcam_url="http://192.168.0.180:4747/video"