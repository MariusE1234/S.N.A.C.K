#File-imports
from layer1.entities import Coin
from layer2.interfaces import IDataAccess, IProductList, ITransactionLog

class TransactionLog(ITransactionLog):
    def __init__(self, data_access: IDataAccess):
        self.data_access = data_access
        self.transactions = self.data_access.get_transactions()


    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.data_access.add_transaction(transaction, transaction.remaining_stock)

    def get_transactions(self):
        return self.transactions

    def get_total_sales(self):
        total_sales = 0
        for transaction in self.transactions:
            total_sales += transaction.product.price
        return total_sales

class ProductList(IProductList):
    def __init__(self, data_access: IDataAccess):
        self.data_access = data_access
        self.products = self.data_access.get_products()

    def save_products(self, products):
        self.data_access.clear_products()  # Löschen Sie vorhandene Produkte in der Datenbank
        self.data_access.save_products(products)
        self.products = products

    def get_products(self):
        return self.products

class CoinSlot:
    def __init__(self):
        self.coins = []

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
        for coin_value in reversed(Coin.available_coins):
            while remaining_amount >= coin_value:
                self.add_coin(Coin(coin_value))
                remaining_amount -= coin_value
        return self.coins

    def reset(self):
        self.coins = []
