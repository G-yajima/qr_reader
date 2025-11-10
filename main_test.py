import sys
import shutil
from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    src_path = "tests/data/TestExcel_org.xlsx"
    path_excel = "TestExcel.xlsx"
    shutil.copy(src_path, path_excel)
    main()
