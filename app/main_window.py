from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QTextEdit, QFileDialog, QMessageBox,
    QLabel, QLineEdit
)
from PyQt6.QtCore import Qt
from src.qr_scanner import qr_scan
from src.rewrite_excel import rewrite_excel

# 背景関連
from PyQt6.QtGui import QPixmap
import sys, os

def resource_path(relative_path):
    """PyInstallerでもPython実行でも画像を正しく読み込むための関数"""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller実行時
        base_path = sys._MEIPASS
    else:
        # 普通にpython main.py 実行時
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")  # ←assetsのある親フォルダに合わせる
    return os.path.join(base_path, relative_path)

# 現在日時取得
import time

# 独自の例外判定
class AlreadyScannedException(Exception):
    def __str__(self):
        return "QRをすでに読み取っています！追加で読み込みたいならエクセルを更新した後にアプリを再起動してね"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # エクセルの必要な列たち
        self.required_cols = ["Label", "Location", "User"]

        self.setWindowTitle("QR Excel Updater 💫")
        self.setGeometry(200, 200, 680, 540)

        # === 背景画像ラベル1 ===
        bg_label1 = QLabel(self)
        bg_pixmap1 = QPixmap(resource_path("assets/background1.png"))
        bg_label1.setPixmap(bg_pixmap1)
        bg_label1.setScaledContents(True)  # ウィンドウサイズに合わせて拡大縮小
        bg_label1.setGeometry(370, 90, 320, 200)

        # === 半透明オーバーレイ ===
        overlay = QLabel(self)
        overlay.setStyleSheet("background-color: rgba(255, 255, 255, 128);")  # 白50%透明
        overlay.setGeometry(0, 0, self.width(), self.height())

        # 背景を一番後ろに固定
        bg_label1.lower()
        overlay.lower()

        # === DroidCam URL入力欄 ===
        self.label_url = QLabel("DroidCamのURL:", self)
        self.label_url.setGeometry(50, 30, 150, 30)

        self.input_url = QLineEdit(self)
        self.input_url.setGeometry(180, 30, 360, 30)
        self.input_url.setPlaceholderText("192.168.0.111:4747")

        # === 出力フォルダ選択欄 ===
        self.label_outdir = QLabel("ログフォルダ:", self)
        self.label_outdir.setGeometry(50, 80, 150, 30)

        self.input_outdir = QLineEdit(self)
        self.input_outdir.setGeometry(180, 80, 260, 30)
        self.input_outdir.setPlaceholderText("例: tests/output")

        self.btn_select_dir = QPushButton("参照...", self)
        self.btn_select_dir.setGeometry(460, 80, 80, 30)
        self.btn_select_dir.clicked.connect(self.select_output_dir)

        # === 調査地入力欄 ===
        self.label_location = QLabel("調査地:", self)
        self.label_location.setGeometry(50, 130, 150, 30)

        self.input_location = QLineEdit(self)
        self.input_location.setGeometry(180, 130, 200, 30)
        self.input_location.setPlaceholderText("例: 房総")

        # === 使用者入力欄 ===
        self.label_user = QLabel("使用者:", self)
        self.label_user.setGeometry(50, 180, 150, 30)

        self.input_user = QLineEdit(self)
        self.input_user.setGeometry(180, 180, 200, 30)
        self.input_user.setPlaceholderText("例: 矢島")

        # === ボタン ===
        self.btn_scan = QPushButton("QR読み取り📷", self)
        self.btn_scan.setGeometry(50, 230, 200, 40)
        self.btn_scan.clicked.connect(self.scan_qr)

        self.btn_rewrite = QPushButton("Excel更新✏️", self)
        self.btn_rewrite.setGeometry(270, 230, 200, 40)
        self.btn_rewrite.clicked.connect(self.update_excel)

        # === ログ欄 ===
        self.text_log = QTextEdit(self)
        self.text_log.setGeometry(50, 290, 580, 200)
        self.text_log.setReadOnly(True)
        self.text_log.setPlaceholderText("ここにログが出るよ✨")

        # === 内部状態 ===
        self.qr_labels = []
        local_time = time.localtime()
        self.to_Date = int(time.strftime("%Y%m%d", local_time))

    def log(self, message):
        """ログ出力"""
        self.text_log.append(message)

    def select_output_dir(self):
        """保存フォルダ選択"""
        directory = QFileDialog.getExistingDirectory(self, "保存フォルダを選択")
        if directory:
            self.input_outdir.setText(directory)
            self.log(f"📁 保存先フォルダ: {directory}")

    def scan_qr(self):
        """QRコード読み取り"""
        ip_and_port = self.input_url.text().strip()
        if not ip_and_port:
            QMessageBox.warning(self, "注意⚠️", "DroidCamのURLを入力してね！")
            return

        url = f"http://{ip_and_port}/video"

        try:
            if len(self.qr_labels) == 0:
                result = qr_scan(url)
                self.qr_labels = result.records
                self.log(f"✅ 読み取ったQRの数: {len(self.qr_labels)}")
            else:
                # すでに読み取り済み
                raise AlreadyScannedException()
        except Exception as e:
            QMessageBox.critical(self, "エラー💥", f"QR読み取り失敗: {e}")

    def update_excel(self):
        """Excelファイルの書き換え"""
        if not self.qr_labels:
            QMessageBox.warning(self, "注意⚠️", "QRを先に読み取ってね！")
            return

        output_dir = self.input_outdir.text().strip()
        if not output_dir:
            QMessageBox.warning(self, "注意⚠️", "保存フォルダを指定してね！")
            return

        to_Location = self.input_location.text().strip()
        if not to_Location:
            QMessageBox.warning(self, "注意⚠️", "調査地を入力してね！")
            return

        to_User = self.input_user.text().strip()
        if not to_User:
            QMessageBox.warning(self, "注意⚠️", "使用者を入力してね！")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Excelファイルを選択", "", "Excel Files (*.xlsx)"
        )
        if not file_path:
            return

        try:
            warning_msg = rewrite_excel(file_path, self.required_cols, output_dir, self.qr_labels, to_Location, to_User, self.to_Date)

            if warning_msg:
                QMessageBox.warning(self, "警告⚠️", warning_msg)
            
            QMessageBox.information(self, "完了✨", "Excelの書き換えが完了しました！")
            self.log(f"✏️ Excel更新完了: {file_path}\n→ ログファイルの保存先: {output_dir}\n→ 調査地: {to_Location}, 使用者: {to_User}")
        except UserWarning as w:
            QMessageBox.warning(self, "警告⚠️", str(w))
        except Exception as e:
            QMessageBox.critical(self, "エラー💥", f"書き換え失敗: {e}")
