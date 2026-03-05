# main.py
import sys
import traceback

from PyQt6.QtWidgets import QApplication

try:
    from database.connection import engine
    from models.firma import Firma
    from models.nastan import Nastan
    from ui.main_window import MainWindow
    print("✅ Imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    traceback.print_exc()
    sys.exit(1)

def main():
    print("🚀 Starting app...")
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(1100, 600)
    win.show()
    print("✅ Window shown")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
#test