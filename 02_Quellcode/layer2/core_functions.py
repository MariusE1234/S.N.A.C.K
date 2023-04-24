#Datei core_functions.py
#File-imports
from layer1.entities import Coin, Transaction, Product
from layer2.interfaces import ITransactionDataAccess, IProductDataAccess, IProductList, ITransactionLog

class TransactionLog(ITransactionLog):
    def __init__(self, data_access: ITransactionDataAccess):
        self.data_access = data_access
        self.transactions = self.data_access.get_transactions()

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.data_access.add_transaction(transaction, transaction.remaining_stock)

    def get_transactions(self):
        return self.transactions

class ProductList(IProductList):
    def __init__(self, data_access: IProductDataAccess):
        self.data_access = data_access
        self.products = self.data_access.get_products()
    
    def delete_products(self):
        self.data_access.clear_products()

    def save_products(self, products):
        self.data_access.save_products(products)
        self.products = products

    def get_products(self):
        return self.products

class CoinManager:
    def __init__(self):
        self.coins = []
    
    def get_availableCoins(self):
        return [Coin(value) for value in Coin.get_availableCoins()]

    def add_coin(self, coin):
        self.coins.append(coin)

    def get_total_amount(self):
        total_amount = 0.0
        for coin in self.coins:
            total_amount += coin.value
        return total_amount

    def sub_coin(self, amount):
        if amount > self.get_total_amount():
            raise ValueError("Betrag ist größer als das verfügbare Guthaben")
        remaining_amount = self.get_total_amount() - amount
        self.reset()
        for coin_value in reversed(Coin.get_availableCoins()):
            while remaining_amount >= coin_value:
                self.add_coin(Coin(coin_value))
                remaining_amount -= coin_value
        return self.coins

    def reset(self):
        self.coins = []

class ProductManager:
    def __init__(self):
        self.selected_product = None

    def select_product(self, product):
        self.selected_product = product

    def get_products(self, product_list: IProductList):
        return product_list.products

    def update_stock(self, product_list: IProductList):
        self.selected_product.stock -= 1
        product_list.delete_products()
        product_list.save_products(product_list.products)
    
    def create_product(self, name, price, stock, image_path):
        return Product(name, price, stock, image_path)
    
    def get_selected_product(self):
        return self.selected_product
    
    def reset_selected_product(self):
        self.selected_product = None

class TransactionManager:
    def __init__(self,transaction_log: ITransactionLog):
        #self.coin_manager = coin_manager
        self.transaction_log = transaction_log

    def add_transaction(self, product):
        remaining_stock = product.stock - 1
        transaction = Transaction(product.name, product.price, remaining_stock)
        self.transaction_log.add_transaction(transaction)
    
    def get_transactions(self):
        return self.transaction_log.get_transactions()
    
    def create_transaction(self, product_name, amount_paid, remaining_stock, timestamp):
        return Transaction(product_name, amount_paid, remaining_stock, timestamp)

class SalesCalculator:
    @staticmethod
    def get_total_sales(transactions):
        total_sales = 0
        for transaction in transactions:
            total_sales += transaction.amount_paid
        return total_sales
    
    @staticmethod
    def get_sold_products(transactions):
        sold_products = 0
        for transaction in transactions:
            sold_products += 1
        return sold_products