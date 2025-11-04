import cv2

def decode_qr(image):
    """画像からQRコードを読み取って文字列を返す"""
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(image)
    return data if data else None