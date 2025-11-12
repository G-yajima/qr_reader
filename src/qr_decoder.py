from pyzbar import pyzbar
import cv2
from collections import defaultdict

def decode_qr_image(image):
    """画像からQRコードまたはバーコードを読み取って文字列を返す"""
    decoded_objects = pyzbar.decode(image)
    if decoded_objects:
        # 最初に見つかったコードを返す（従来仕様に合わせて1つだけ）
        return decoded_objects[0].data.decode('utf-8')
    return None


class QrDecorder():
    def __init__(self, droidcam_url=None):
        self.droidcam_url = droidcam_url
        self.state = "run"
        self.current_codes = set()

    def decode_droidcam(self, confirmation_threshold=5):
        """
        DroidCamから複数のQR/バーコードをリアルタイムプレビューしながら読み取る
        """
        cap = cv2.VideoCapture()
        if not cap.open(self.droidcam_url):
            raise ConnectionError(f"カメラ({self.droidcam_url})に接続できませんでした")
        
        # 検出回数カウント
        detection_count = defaultdict(int)
        confirmed_qr_codes = set()

        if len(self.current_codes) != 0:
            previous_codes = self.current_codes
            confirmed_qr_codes.update(list(self.current_codes))

        frame_count = 0
        
        print("=" * 60)
        print("DroidCam 複数QR/バーコードリーダー")
        print("=" * 60)
        print(f"設定: {confirmation_threshold}回以上検出されたコードを確定")
        print("操作方法:")
        print("  [Enter] 読み取りを終了")
        print("  [ESC]   キャンセル")
        print("=" * 60)
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    raise RuntimeError("フレームの取得に失敗しました")

                frame_count += 1
                display_frame = frame.copy()
                current_frame_qr_codes = []

                # pyzbarでコードを検出（QR, EAN, CODE128など）
                decoded_objects = pyzbar.decode(frame)

                if decoded_objects:
                    for obj in decoded_objects:
                        data = obj.data.decode("utf-8")
                        current_frame_qr_codes.append(data)
                        detection_count[data] += 1

                        if detection_count[data] >= confirmation_threshold:
                            confirmed_qr_codes.add(data)

                        # バウンディングボックスを描画
                        (x, y, w, h) = obj.rect
                        if data in confirmed_qr_codes:
                            color = (0, 255, 0)  # 緑
                            status = "CONFIRMED"
                        else:
                            color = (0, 255, 255)  # 黄色
                            status = f"{detection_count[data]}/{confirmation_threshold}"
                        
                        cv2.rectangle(display_frame, (x, y), (x + w, y + h), color, 3)
                        cv2.putText(display_frame, status,
                                    (x, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                # 情報表示エリア
                overlay = display_frame.copy()
                info_height = 125
                cv2.rectangle(overlay, (5, 5), (600, info_height), (50, 50, 50), -1)
                cv2.addWeighted(overlay, 0.7, display_frame, 0.3, 0, display_frame)
                
                y_offset = 25
                cv2.putText(display_frame, f"Confirmed Codes: {len(confirmed_qr_codes)}", 
                        (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                y_offset += 25
                cv2.putText(display_frame, f"Currently Detecting: {len(current_frame_qr_codes)}", 
                        (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
                
                y_offset += 30
                cv2.putText(display_frame, "Press [ENTER] to finish", 
                        (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 200, 255), 1)
                
                cv2.imshow('DroidCam - Multiple Code Reader', display_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == 13:  # Enter
                    self.state = "stop"
                    break
                elif key == 27:  # ESC
                    print("\n✗ キャンセルされました")
                    confirmed_qr_codes = set()
                    confirmed_qr_codes.update(list(previous_codes))
                    break

        except Exception as e:
            print(f"⚠️ エラー: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()

        if self.state == "stop":
            self.current_codes = set()
            self.current_codes.update(list(confirmed_qr_codes))
