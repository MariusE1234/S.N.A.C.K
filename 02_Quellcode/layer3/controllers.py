#Datei controllers.py
#File-imports
from layer2.interfaces import IConfigDataAccess,IProductDataAccess, ITransactionDataAccess, IDatabase
from layer2.core_functions import SalesCalculator, ProductManager,TransactionManager, CoinManager, TransactionLog, ProductList
from layer2.vending_machine import VendingMachine

class VendingMachineController:
    def __init__(self, db: IDatabase, coinmanager, transactionmanager):
        self.product_data_access = db.get_ProductDataAccess()
        self.transaction_data_access = db.get_TransactionDataAccess()
        self.config_data_access = db.get_ConfigDataAccess()
        self.product_list = ProductList(self.product_data_access)
        self.coin_manager = coinmanager
        self.transactionmanager = transactionmanager
        self.observers = []
        self.vending_machine = VendingMachine(self.product_list, self.coin_manager, self.transactionmanager)

    
    def add_observer(self, observer):
        self.observers.append(observer)
        
    def notify_observers(self, notification_type, *args):
        for observer in self.observers:
            observer.update(notification_type, *args)
            
    def get_products(self):
        return self.vending_machine.get_products()

    def select_product(self, product):
        self.vending_machine.select_product(product)

    def get_productList(self):
        return self.product_list

    def buy_product(self):
        return self.vending_machine.buy_product()

    def get_total_amount(self):
        return self.coin_manager.get_total_amount()

class ConfigController:
    def __init__(
        self,
        config_data_access: IConfigDataAccess,
    ):
        self.config_data_access = config_data_access

    def update_config(self, value, new_pin):
        self.config_data_access.update_config(value, new_pin)
    
class TransactionController:
    def __init__(self, transaction_data_access: ITransactionDataAccess): 
        self.transactionLog = TransactionLog(transaction_data_access)
        self.transactionmanager = TransactionManager(self.transactionLog)
    
    def get_transactions(self):
        return self.transactionmanager.get_transactions()
    
    def add_transaction(self, product):
        self.transactionmanager.add_transaction(product)
    
class StatController:
    def __init__(self, transactioncontroller):
        self.salesCalc = SalesCalculator()
        self.transactioncontroller = transactioncontroller

    def get_total_sales(self):
        return self.salesCalc.get_total_sales(self.transactioncontroller.get_transactions())
    
    def get_sold_products(self):
        return self.salesCalc.get_sold_products(self.transactioncontroller.get_transactions())

class CoinController:
    def __init__(self): 
        self.coin_manager = CoinManager() 

    def get_availableCoins(self):
        return self.coin_manager.get_availableCoins() 

    def add_coin(self, coin):
        self.coin_manager.add_coin(coin)

    def get_total_amount(self):
        return self.coin_manager.get_total_amount()

    def sub_coin(self, amount):
        self.coin_manager.sub_coin(amount)

    def reset(self):
        self.coin_manager.reset()

class ProductController:
    def __init__(self, product_data_access: IProductDataAccess = None,): 
        self.product_manager = ProductManager() 
        self.product_data_access = product_data_access

    def create_product(self, name, price, stock, image_path):
        return self.product_manager.create_product(name, price, stock, image_path)
    
    def add_product(self, new_product, product_table):
        if self.is_name_unique(new_product.name, product_table, self):
            self.product_data_access.add_product(new_product)
            return True
        else:
            return False

    def edit_product(self, current_product, edited_product, product_table, exclude_row=None):
        if self.is_name_unique(edited_product.name, product_table, exclude_row):
            self.product_data_access.update_product(current_product, edited_product)
            return True
        else:
            return False

    def delete_product(self, product_name):
        self.product_data_access.delete_product(product_name)

    def get_products(self):
        return self.product_data_access.get_products()
        
    def get_products_from_table(self, product_table):
        products = []
        for i in range(product_table.rowCount()):
            name_item = product_table.item(i, 0)
            price_item = product_table.item(i, 1)
            stock_item = product_table.item(i, 2)
            image_item = product_table.item(i, 3)
            if name_item is not None and price_item is not None and stock_item is not None:
                products.append(self.product_manager.create_product(name_item.text(), float(price_item.text()), int(stock_item.text()),image_item.text()))
        return products

    def is_name_unique(self, name, product_table, exclude_row=None):
        for row in range(product_table.rowCount()):
            if row != exclude_row and product_table.item(row, 0).text() == name:
                return False
        return True