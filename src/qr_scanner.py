import keyboard
import time
from src.qr_decoder import QrDecorder
from src.qr_recorder import QrRecorder

def qr_scan(droidcam_url):
    """
    スペースキーが押されるまでQRコードを繰り返し読み取る
    
    Args:
        droidcam_url: DroidCamのURL
        stop_key: 停止するキー（デフォルト: 'space'）
    """
    r = QrRecorder()
    d = QrDecorder(droidcam_url)
    scan_count = 0
    
    print("=" * 60)
    print("連続QRコードスキャンモード")
    print("=" * 60)
    print("=" * 60)
    
    while True:
        # エンターキーが押されたら終了
        if d.state == "stop":
            break
        
        scan_count += 1
        # print(f"\n--- スキャン #{scan_count} ---")
        
        try:
            d.decode_droidcam()
            results = list(d.current_codes)
            
            if results:
                # new_codes = [code for code in results if code not in r.records]
                r.add_decodes(results)
                
            if d.state == "stop":
                break
        
        except ConnectionError as e:
            # print(f"⚠ 接続エラー: {e}")
            # print("  再接続を試みます...")
            time.sleep(2)
        
        except Exception as e:
            # print(f"⚠ エラー: {e}")
            time.sleep(1)
        
        # 次のスキャンまで少し待機
        time.sleep(0.5)
    
    # 最終結果を表示
    print("\n" + "=" * 60)
    print("スキャン完了")
    print("=" * 60)
    print(f"総スキャン回数: {scan_count}")
    print(f"記録されたQRコード: {len(r.records)}個")
    
    return r