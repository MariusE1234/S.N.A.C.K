import sys
import PyQt5
import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QTableWidgetItem, QPushButton, QGridLayout, QVBoxLayout, QTableWidget, QWidget

class Transaction:
    def __init__(self, product, amount_paid):
        self.product = product
        self.amount_paid = amount_paid
        self.timestamp = datetime.datetime.now()

    def __str__(self):
        return f"{self.timestamp}: {self.product} - {self.amount_paid} €"


class TransactionLog:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions

    def get_total_sales(self):
        total_sales = 0
        for transaction in self.transactions:
            total_sales += transaction.product.price
        return total_sales

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} ({self.price} €)"

class ProductList:
    def __init__(self):
        self.products = [
            Product("Cola", 1.5),
            Product("Fanta", 1.5),
            Product("Sprite", 1.5),
            Product("Chips", 0.75),
            Product("Schokoriegel", 0.5),
            Product("Kaugummi", 0.2)
        ]

class Coin:
    available_coins = [0.05, 0.1, 0.2, 0.5, 1, 2]

    def __init__(self, value):
        if value in Coin.available_coins:
            self.value = value
        else:
            raise ValueError("Ungültiger Münzwert")

    def __str__(self):
        return f"{self.value} €"


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
    def __init__(self, product_list, coin_slot, transaction_log):  # Dependency Injection
        self.product_list = product_list
        self.coin_slot = coin_slot
        self.transaction_log = transaction_log
        self.selected_product = None

    def select_product(self, product):
        self.selected_product = product

    def buy_product(self):
        if self.selected_product is None:
            return "Bitte wählen Sie ein Produkt aus."
        if self.selected_product.price > self.coin_slot.get_total_amount():
            return "Sie haben nicht genug Geld eingeworfen."
        self.coin_slot.sub_coin(self.selected_product.price)
        product_bought = self.selected_product.name
        transaction = Transaction(self.selected_product, self.selected_product.price)
        self.transaction_log.add_transaction(transaction)
        self.selected_product = None
        return f"Vielen Dank für Ihren Einkauf: {product_bought}"

    def get_products(self):
        return self.product_list.products

class CoinsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Münzen einwerfen")
        self.coins = [Coin(value) for value in Coin.available_coins]
        self.selected_coin = None
        self.setup_ui()

    def setup_ui(self):
        self.coin_buttons = []
        layout = QGridLayout()

        for i, coin in enumerate(self.coins):
            button = QPushButton(str(coin))
            button.clicked.connect(lambda _, c=coin: self.select_coin(c))
            self.coin_buttons.append(button)
            layout.addWidget(button, i // 2, i % 2)

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button, len(self.coins) // 2, 0)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button, len(self.coins) // 2, 1)

        self.setLayout(layout)

    def select_coin(self, coin):
        self.selected_coin = coin

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Konfigurationsmenü")
        self.product_list = ProductList()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(2)
        self.product_table.setHorizontalHeaderLabels(["Produkt", "Preis"])
        self.product_table.verticalHeader().setVisible(False)

        for i, product in enumerate(self.product_list.products):
            name_item = QTableWidgetItem(product.name)
            price_item = QTableWidgetItem(str(product.price))
            self.product_table.setItem(i, 0, name_item)
            self.product_table.setItem(i, 1, price_item)

        self.product_table.resizeColumnsToContents()
        layout.addWidget(self.product_table)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_products(self):
        products = []
        for i in range(self.product_table.rowCount()):
            name_item = self.product_table.item(i, 0)
            price_item = self.product_table.item(i, 1)
            if name_item is not None and price_item is not None:
                products.append(Product(name_item.text(), float(price_item.text())))
        return products

class VendingMachineGUI(QWidget):
    def __init__(self):
        super().__init__()
        product_list = ProductList()
        coin_slot = CoinSlot()
        transaction_log = TransactionLog()
        self.vending_machine = VendingMachine(product_list, coin_slot, transaction_log)  # Dependency Injection
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("S.N.A.C.K Verkaufsautomat")
        self.product_buttons = []
        layout = QGridLayout()

        for i, product in enumerate(self.vending_machine.get_products()):
            button = QPushButton(str(product))
            button.clicked.connect(lambda _, p=product: self.select_product(p))
            self.product_buttons.append(button)
            layout.addWidget(button, i // 3, i % 3)

        self.coin_button = QPushButton("Münzen einwerfen")
        self.coin_button.clicked.connect(self.show_coin_dialog)
        layout.addWidget(self.coin_button, len(self.product_buttons) // 3 + 1, 0)

        self.config_button = QPushButton("Konfigurationsmenü")
        self.config_button.clicked.connect(self.show_config_dialog)
        layout.addWidget(self.config_button, len(self.product_buttons) // 3 + 1, 1)

        self.buy_button = QPushButton("Kaufen")
        self.buy_button.clicked.connect(self.buy_product)
        layout.addWidget(self.buy_button, len(self.product_buttons) // 3 + 1, 2)

        self.coin_label = QLabel("0.0 €")
        layout.addWidget(self.coin_label, len(self.product_buttons) // 3 + 2, 0)

        self.status_label = QLabel("Bitte wählen Sie ein Produkt aus.")
        layout.addWidget(self.status_label, len(self.product_buttons) // 3 + 2, 1, 1, 2)

        self.setLayout(layout)

    def select_product(self, product):
        self.vending_machine.select_product(product)
        self.status_label.setText(f"Bitte werfen Sie {self.vending_machine.selected_product.price} € ein.")

    def buy_product(self):
        message = self.vending_machine.buy_product()
        self.status_label.setText(message)
        #CHECK---------------------------
        amount = f"{self.vending_machine.coin_slot.get_total_amount()} €"
        self.coin_label.setText(str(amount))
        #--------------------------------

    def show_coin_dialog(self):
        dialog = CoinsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.vending_machine.coin_slot.add_coin(dialog.selected_coin)
            self.coin_label.setText(f"{self.vending_machine.coin_slot.get_total_amount()} €")
    
    def show_config_dialog(self):
        dialog = ConfigDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.vending_machine.product_list.products = dialog.get_products()
            self.setup_ui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VendingMachineGUI()
    gui.show()
    sys.exit(app.exec_())
