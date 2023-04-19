from abc import ABC, abstractmethod
from entities import Transaction, Product, Coin
from interface_adapters import IDataAccess

class ITransactionLog(ABC):
    @abstractmethod
    def add_transaction(self, transaction):
        pass

    @abstractmethod
    def get_transactions(self):
        pass

    @abstractmethod
    def get_total_sales(self):
        pass

class IProductList(ABC):
    @abstractmethod
    def save_products(self, products):
        pass

    @abstractmethod
    def get_products(self):
        pass

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

class VendingMachine:
    def __init__(
        self,
        product_list: IProductList,
        coin_slot,
        data_access: IDataAccess,
    ):  # Dependency Injection
        self.product_list = product_list
        self.coin_slot = coin_slot
        self.data_access = data_access
        self.transaction_log = TransactionLog(data_access)
        self.selected_product = None

    def select_product(self, product):
        self.selected_product = product

    def buy_product(self):
        if self.selected_product is None:
            return "Bitte wählen Sie ein Produkt aus."
        if self.selected_product.price > self.coin_slot.get_total_amount():
            return "Sie haben nicht genug Geld eingeworfen."
        if self.selected_product.stock <= 0:
            return "Dieses Produkt ist leider nicht mehr vorrätig."

        self.coin_slot.sub_coin(self.selected_product.price)
        product_bought = self.selected_product.name
        remaining_stock = self.selected_product.stock - 1
        transaction = Transaction(
            self.selected_product.name, self.selected_product.price, remaining_stock
        )
        self.transaction_log.add_transaction(transaction)

        # Bestand aktualisieren
        self.selected_product.stock -= 1
        self.product_list.save_products(self.product_list.products)

        self.selected_product = None
        return f"Vielen Dank für Ihren Einkauf: {product_bought}"

    def get_products(self):
        return self.product_list.products
