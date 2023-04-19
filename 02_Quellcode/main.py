import sys
from frameworks_and_drivers import VendingMachineGUI
from PyQt5.QtWidgets import QApplication

db_path = "03_SQL//database//vendingMachine.db"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VendingMachineGUI(db_path)
    gui.show()
    sys.exit(app.exec_())
