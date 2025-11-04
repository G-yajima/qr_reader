import cv2

def decode_qr_image(image):
    """画像からQRコードを読み取って文字列を返す"""
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(image)
    return data if data else None

import cv2
from collections import defaultdict

def decode_qr_droidcam(droidcam_url, confirmation_threshold=5):
    """
    DroidCamから複数のQRコードをリアルタイムプレビューしながら読み取る
    
    Args:
        droidcam_url: DroidCamのURL
        confirmation_threshold: QRコードを確定するために必要な検出回数
    
    Returns:
        list: 読み取ったQRコードのデータのリスト
    
    操作方法:
    - QRコードを検出したら画面に表示される
    - n回以上検出されたQRコードは確定される
    - Enterキーを押すと読み取りを終了
    - ESCキーを押すとキャンセル
    """
    cap = cv2.VideoCapture()
    
    if not cap.open(droidcam_url):
        raise ConnectionError(f"カメラ({droidcam_url})に接続できませんでした")
    
    qr_detector = cv2.QRCodeDetector()
    
    # QRコードの検出回数をカウント
    detection_count = defaultdict(int)
    
    # 確定したQRコードのセット
    confirmed_qr_codes = set()
    
    frame_count = 0
    
    print("=" * 60)
    print("DroidCam 複数QRコードリーダー")
    print("=" * 60)
    print(f"設定: {confirmation_threshold}回以上検出されたQRコードを確定")
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
            
            # 複数のQRコードを検出
            success, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(frame)
            
            # 表示用のフレームをコピー
            display_frame = frame.copy()
            
            # 現在のフレームで検出されたQRコード
            current_frame_qr_codes = []
            
            if success and decoded_info:
                for i, data in enumerate(decoded_info):
                    if data:  # 空でないデータのみ処理
                        current_frame_qr_codes.append(data)
                        
                        # 検出回数をカウント
                        detection_count[data] += 1
                        
                        # 確定条件を満たしたか確認
                        if detection_count[data] >= confirmation_threshold:
                            confirmed_qr_codes.add(data)
                        
                        # QRコードの領域を描画
                        if points is not None and len(points) > i:
                            bbox = points[i].astype(int)
                            
                            # 確定済みなら緑、未確定なら黄色
                            if data in confirmed_qr_codes:
                                color = (0, 255, 0)  # 緑
                                status = "CONFIRMED"
                            else:
                                color = (0, 255, 255)  # 黄色
                                status = f"{detection_count[data]}/{confirmation_threshold}"
                            
                            cv2.polylines(display_frame, [bbox], True, color, 3)
                            
                            # QRコードの位置にテキストを表示
                            text_pos = tuple(bbox[0])
                            cv2.putText(display_frame, status, 
                                       (text_pos[0], text_pos[1] - 10),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # 情報表示エリア
            overlay = display_frame.copy()
            info_height = 100 + len(confirmed_qr_codes) * 25
            cv2.rectangle(overlay, (5, 5), (600, info_height), (50, 50, 50), -1)
            cv2.addWeighted(overlay, 0.7, display_frame, 0.3, 0, display_frame)
            
            # ヘッダー情報
            y_offset = 25
            cv2.putText(display_frame, f"Confirmed QR Codes: {len(confirmed_qr_codes)}", 
                       (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            y_offset += 25
            cv2.putText(display_frame, f"Currently Detecting: {len(current_frame_qr_codes)}", 
                       (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            
            # 確定したQRコードのリストを表示
            if confirmed_qr_codes:
                y_offset += 30
                cv2.putText(display_frame, "Confirmed QR codes:", 
                           (10, y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
                for idx, qr_data in enumerate(sorted(confirmed_qr_codes), 1):
                    y_offset += 20
                    display_text = f"{idx}. {qr_data[:40]}..." if len(qr_data) > 40 else f"{idx}. {qr_data}"
                    cv2.putText(display_frame, display_text, 
                               (20, y_offset),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
            # 操作ガイド
            y_offset += 30
            cv2.putText(display_frame, "Press [ENTER] to finish", 
                       (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 200, 255), 1)
            
            # ウィンドウに表示
            cv2.imshow('DroidCam - Multiple QR Code Reader', display_frame)
            
            # キー入力待ち
            key = cv2.waitKey(1) & 0xFF
            
            if key == 13:  # Enterキー
                print(f"\n✓ 読み取り終了!")
                print(f"  確定したQRコード数: {len(confirmed_qr_codes)}")
                break
            elif key == 27:  # ESCキー
                print("\n✗ キャンセルされました")
                confirmed_qr_codes = set()
                break
        
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # リストとして返す
    detected_data = list(confirmed_qr_codes)
    return detected_data