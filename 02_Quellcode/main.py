import sys
from frameworks_and_drivers import VendingMachineGUI
from PyQt5.QtWidgets import QApplication
from database import Database


if __name__ == "__main__":

    app = QApplication(sys.argv)
    gui = VendingMachineGUI(Database())
    gui.show()
    sys.exit(app.exec_())
