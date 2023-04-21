#File-imports
from layer3.database import Database
from layer3.controllers import VendingMachineController
from layer3.factorys import DefaultProductButtonFactory, DefaultCoinsDialogFactory, DefaultPinDialogFactory, DefaultConfigDialogFactory, DefaultInfoDialogFactory
from layer3.ui import VendingMachineGUI
#libraries-imports
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":

    db = Database()
    vmcontroller = VendingMachineController(db)

    app = QApplication(sys.argv)
    gui = VendingMachineGUI(
        vmcontroller, 
        DefaultProductButtonFactory(), 
        DefaultCoinsDialogFactory(), 
        DefaultPinDialogFactory(), 
        DefaultConfigDialogFactory(), 
        DefaultInfoDialogFactory()
        )
    
    gui.show()
    sys.exit(app.exec_())
