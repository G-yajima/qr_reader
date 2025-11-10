# テストコマンド
## QRを実際に読み込まないテストのみ
読み込みはモックしてる。
pytest -v -m "not integration"

## 統合テストのみ
pytest -v -m "integration" --droidcam_url="http://192.168.0.180:4747/video"

## すべて
pytest -v --droidcam_url="http://192.168.0.180:4747/video"

# exe化
pyinstaller --noconsole --onefile --add-data "assets;assets" main.p


# ToDoリスト
- [o] 接続が不安定そうなので、落ちても記録が残るように改良
    - [o] recoder classを定義
        - [o] これまで記録してきたconfirmed_qr_codes（set class）を格納
    - [o] 再度 QRを読み取るときは、これまでの結果を渡す
        - [o] decorderにもクラスが必要？ -> 作った
    - [o] 特定のキーを押すまでwhileでクラスを維持
        - [o] スペースを押してもち中断されない -> エンターで中止するよう変更

- エクセルの形式チェック
    - [o] Label Location Userを含めば、あとは自由に
    - [o] 上記3点セットがそろってるか確認 -> なければエラー

- GUIへの要望
    - [o] 画面の端とかに、読み込んだ数とかを表示するように
    - [o] 保存フォルダ（名前もログフォルダにしたほうがいいかも）を選択しない、をできるように
        - これは必須にした。名前はログフォルダへ

- 接続について
    - [o] 読み取りを開始して読み取りができなかったときに固まる
        - 何秒かたっても接続できない場合は、待機画面に戻るようにすればよい？
        - そんなことない？一応解決？

- GUI
    - [0] リストにないSDの出力表示
    - [o] 更新日時追加

