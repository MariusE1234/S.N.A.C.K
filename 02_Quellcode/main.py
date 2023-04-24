#Datei main.py
#File-imports
from layer3.database import Database
from layer3.controllers import VendingMachineController, ConfigController, StatController, CoinController, ProductController, TransactionController
from layer3.factories import DefaultProductButtonFactory, DefaultCoinsDialogFactory, DefaultPinDialogFactory, DefaultConfigDialogFactory, DefaultInfoDialogFactory
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
    
    productcontroller = ProductController(db.get_ProductDataAccess())
    transactioncontroller = TransactionController(db.get_TransactionDataAccess())
    statcontroller = StatController(transactioncontroller)
    coincontroller = CoinController()
    configcontroller = ConfigController(db.get_ConfigDataAccess())
    vmcontroller = VendingMachineController(db, coincontroller, transactioncontroller)
    

    app = QApplication(sys.argv)
    gui = VendingMachineGUI(
        vmcontroller,
        configcontroller,
        statcontroller,
        coincontroller,
        productcontroller,
        transactioncontroller,
        DefaultProductButtonFactory(),
        DefaultCoinsDialogFactory(),
        DefaultPinDialogFactory(),
        DefaultConfigDialogFactory(),
        DefaultInfoDialogFactory()
    )

    gui.show()
    sys.exit(app.exec_())
