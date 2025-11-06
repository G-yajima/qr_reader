from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QTextEdit, QFileDialog, QMessageBox, QLabel, QLineEdit
)
from PyQt6.QtCore import Qt

# あーしの関数たちをimport（実際のファイル名に合わせてね！）
from src.qr_scanner import qr_scan
from src.rewrite_excel import rewrite_excel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Excel Updater 💫")
        self.setGeometry(200, 200, 600, 420)

        # === DroidCam URL入力欄 ===
        self.label_url = QLabel("DroidCamのURL:", self)
        self.label_url.setGeometry(50, 30, 150, 30)

        self.input_url = QLineEdit(self)
        self.input_url.setGeometry(180, 30, 360, 30)
        self.input_url.setPlaceholderText("192.168.0.111:4747")

        # === ボタン ===
        self.btn_scan = QPushButton("QR読み取り📷", self)
        self.btn_scan.setGeometry(50, 80, 200, 40)
        self.btn_scan.clicked.connect(self.scan_qr)

        self.btn_rewrite = QPushButton("Excel更新✏️", self)
        self.btn_rewrite.setGeometry(50, 140, 200, 40)
        self.btn_rewrite.clicked.connect(self.update_excel)

        # === ログ欄 ===
        self.text_log = QTextEdit(self)
        self.text_log.setGeometry(50, 200, 500, 180)
        self.text_log.setReadOnly(True)
        self.text_log.setPlaceholderText("ここにログが出るよ✨")

        # === 内部状態 ===
        self.qr_labels = []

    def log(self, message):
        """ログ出力"""
        self.text_log.append(message)

    def scan_qr(self):
        """QRコード読み取り"""
        ip_and_port = self.input_url.text().strip()
        url = "http://" + ip_and_port + "/video"
        if not url:
            QMessageBox.warning(self, "注意⚠️", "DroidCamのURLを入力してね！")
            return

        try:
            result = qr_scan(url)
            self.qr_labels = result.records
            self.log(f"✅ 読み取ったQR: {self.qr_labels}")
        except Exception as e:
            QMessageBox.critical(self, "エラー💥", f"QR読み取り失敗: {e}")

    def update_excel(self):
        """Excelファイルの書き換え"""
        if not self.qr_labels:
            QMessageBox.warning(self, "注意⚠️", "QRを先に読み取ってね！")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Excelファイルを選択", "", "Excel Files (*.xlsx)"
        )
        if not file_path:
            return

        try:
            rewrite_excel(file_path, "logs", self.qr_labels, "房総", "松岡")
            QMessageBox.information(self, "完了✨", "Excelの書き換えが完了しました！")
            self.log(f"✏️ Excel更新完了: {file_path}")
        except UserWarning as w:
            QMessageBox.warning(self, "警告⚠️", str(w))
        except Exception as e:
            QMessageBox.critical(self, "エラー💥", f"書き換え失敗: {e}")
