import keyboard
import time
from src.qr_decoder import decode_qr_droidcam
from src.qr_recorder import QrRecorder

def qr_scan(droidcam_url, stop_key='space'):
    """
    スペースキーが押されるまでQRコードを繰り返し読み取る
    
    Args:
        droidcam_url: DroidCamのURL
        stop_key: 停止するキー（デフォルト: 'space'）
    """
    r = QrRecorder()
    scan_count = 0
    
    print("=" * 60)
    print("連続QRコードスキャンモード")
    print("=" * 60)
    print(f"[{stop_key.upper()}] キーを押すと終了します")
    print("=" * 60)
    
    while True:
        # スペースキーが押されたら終了
        if keyboard.is_pressed(stop_key):
            print(f"\n[{stop_key.upper()}] キーが押されました。終了します...")
            break
        
        scan_count += 1
        print(f"\n--- スキャン #{scan_count} ---")
        
        try:
            results = decode_qr_droidcam(droidcam_url)
            
            if results:
                new_codes = [code for code in results if code not in r.records]
                r.add_decodes(results)
                
                print(f"✓ 検出: {len(results)}個")
                if new_codes:
                    print(f"  新規: {len(new_codes)}個")
                    for code in new_codes:
                        print(f"    - {code}")
                print(f"  累計: {len(r.records)}個")
            else:
                print("✗ QRコードが検出されませんでした")
        
        except ConnectionError as e:
            print(f"⚠ 接続エラー: {e}")
            print("  再接続を試みます...")
            time.sleep(2)
        
        except Exception as e:
            print(f"⚠ エラー: {e}")
            time.sleep(1)
        
        # 次のスキャンまで少し待機
        time.sleep(0.5)
    
    # 最終結果を表示
    print("\n" + "=" * 60)
    print("スキャン完了")
    print("=" * 60)
    print(f"総スキャン回数: {scan_count}")
    print(f"記録されたQRコード: {len(r.records)}個")
    
    if r.records:
        print("\n記録されたQRコード一覧:")
        for i, code in enumerate(r.records, 1):
            print(f"  {i}. {code}")
    
    return r