#File-imports
from layer3.database import Database
from layer3.gui import VendingMachineGUI
from layer3.factorys import DefaultProductButtonFactory, DefaultDialogFactory
#libraries-imports
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":

    app = QApplication(sys.argv)
    gui = VendingMachineGUI(Database(), DefaultProductButtonFactory(), DefaultDialogFactory())
    gui.show()
    sys.exit(app.exec_())
