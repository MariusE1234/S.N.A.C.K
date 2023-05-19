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

# db_path = "03_SQL//database//vendingMachine.db"

def create_database_connection(db_path):
    conn = sqlite3.connect(db_path)
    return Database(ProductDataAccess(conn), TransactionDataAccess(conn), ConfigDataAccess(conn))

class ControllerFactory:
    def __init__(self, db):
        self.db = db

    def create_controllers(self):
        productcontroller = ProductController(self.db.get_ProductDataAccess())
        transactioncontroller = TransactionController(self.db.get_TransactionDataAccess())
        statcontroller = StatController(transactioncontroller)
        coincontroller = CoinController()
        configcontroller = ConfigController(self.db.get_ConfigDataAccess())
        vmcontroller = VendingMachineController(self.db, coincontroller, transactioncontroller)
        return vmcontroller, configcontroller, statcontroller, coincontroller, productcontroller, transactioncontroller

if __name__ == "__main__":
    db = create_database_connection("03_SQL//database//vendingMachine.db")    
    factory = ControllerFactory(db)
    vmcontroller, configcontroller, statcontroller, coincontroller, productcontroller, transactioncontroller = factory.create_controllers()
    
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
