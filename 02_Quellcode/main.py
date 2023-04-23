#Datei main.py
#File-imports
from layer3.database import Database
from layer3.controllers import VendingMachineController
from layer3.factorys import DefaultProductButtonFactory, DefaultCoinsDialogFactory, DefaultPinDialogFactory, DefaultConfigDialogFactory, DefaultInfoDialogFactory
from layer3.data_access import ProductDataAccess, TransactionDataAccess, ConfigDataAccess
from layer3.ui import VendingMachineGUI
#libraries-imports
import sys
from PyQt5.QtWidgets import QApplication
import sqlite3

db_path = "03_SQL//database//vendingMachine.db"

if __name__ == "__main__":
    conn = sqlite3.connect(db_path)
    db = Database(ProductDataAccess(conn), TransactionDataAccess(conn), ConfigDataAccess(conn))
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
