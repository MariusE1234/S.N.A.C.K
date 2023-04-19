#File-imports
from layer3.database import Database
from layer3.gui import VendingMachineGUI
#libraries-imports
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":

    app = QApplication(sys.argv)
    gui = VendingMachineGUI(Database())
    gui.show()
    sys.exit(app.exec_())
