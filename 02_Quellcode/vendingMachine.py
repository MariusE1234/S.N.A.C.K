import sys
import PyQt5
import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QTableWidgetItem, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QTableWidget, QScrollArea, QListWidget, QWidget
import sqlite3
from sqlite3 import Error

db_path = "C://Users//Marius//Documents//GitHub//S.N.A.C.K//03_SQL//database//vendingMachine.db"

class Database:
    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)
        self.cur = self.conn.cursor()
        self.create_products_table()

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    def create_products_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS products (
                                name TEXT PRIMARY KEY,
                                price REAL NOT NULL
                              );""")
        except Error as e:
            print(e)

    def add_product(self, product):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (product.name, product.price))
            self.conn.commit()
        except Error as e:
            print(e)

    def get_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, price FROM products")
        rows = cursor.fetchall()

        products = [Product(row[0], row[1]) for row in rows]
        return products

    def update_product(self, old_product, new_product):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE products SET name = ?, price = ? WHERE name = ?", (new_product.name, new_product.price, old_product.name))
            self.conn.commit()
        except Error as e:
            print(e)

    def delete_product(self, product):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM products WHERE name = ?", (product.name,))
            self.conn.commit()
        except Error as e:
            print(e)

    def save_products(self, products):
        with self.conn:
            for product in products:
                # Prüfen, ob ein Produkt mit demselben Namen bereits in der Datenbank vorhanden ist
                self.cur.execute("SELECT COUNT(*) FROM products WHERE name=?", (product.name,))
                count = self.cur.fetchone()[0]

                if count == 0:
                    # Fügen Sie das Produkt hinzu, wenn es noch nicht in der Datenbank vorhanden ist
                    self.cur.execute("INSERT INTO products (name, price) VALUES (?, ?)", (product.name, product.price))
                else:
                    # Aktualisieren Sie den Eintrag, wenn das Produkt bereits in der Datenbank vorhanden ist
                    self.cur.execute("UPDATE products SET price=? WHERE name=?", (product.price, product.name))


class Transaction:
    def __init__(self, product, amount_paid):
        self.product = product
        self.amount_paid = amount_paid
        self.timestamp = datetime.datetime.now()

    def __str__(self):
        formatted_timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")  # Format ohne Nachkommastellen
        return f"{formatted_timestamp} : {self.product.name} {self.amount_paid} €"


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
    def __init__(self, database):
        self.database = database
        self.products = self.database.get_products()

    def save_products(self, products):
        self.database.save_products(products)
        self.products = products

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
    def __init__(self, parent=None, transaction_log=None, product_list=None):
        super().__init__(parent)
        self.setWindowTitle("Konfigurationsmenü")
        self.product_list = product_list
        self.transaction_log = transaction_log
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()

        # Produkte
        product_layout = QVBoxLayout()
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(2)
        self.product_table.setRowCount(len(self.product_list.products))
        self.product_table.setHorizontalHeaderLabels(["Produkt", "Preis"])
        self.product_table.verticalHeader().setVisible(False)

        for i, product in enumerate(self.product_list.products):
            name_item = QTableWidgetItem(product.name)
            price_item = QTableWidgetItem(str(product.price))
            self.product_table.setItem(i, 0, name_item)
            self.product_table.setItem(i, 1, price_item)

        self.product_table.resizeColumnsToContents()
        product_layout.addWidget(self.product_table)

        # Schaltflächen zum Hinzufügen und Löschen von Produkten
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Produkt hinzufügen")
        self.add_button.clicked.connect(self.add_product)
        button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Produkt löschen")
        self.delete_button.clicked.connect(self.delete_product)
        button_layout.addWidget(self.delete_button)

        product_layout.addLayout(button_layout)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        product_layout.addWidget(self.ok_button)

        layout.addLayout(product_layout)

        # Transaktionen
        transaction_layout = QVBoxLayout()
        transaction_label = QLabel("Transaktionen")
        transaction_layout.addWidget(transaction_label)

        self.transaction_list = QListWidget()
        if self.transaction_log:
            for transaction in self.transaction_log.get_transactions():
                self.transaction_list.addItem(str(transaction))

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.transaction_list)
        transaction_layout.addWidget(scroll_area)

        layout.addLayout(transaction_layout)
        self.setLayout(layout)

    def add_product(self):
        row = self.product_table.rowCount()
        self.product_table.setRowCount(row + 1)

    def delete_product(self):
        row = self.product_table.currentRow()
        if row != -1:
            self.product_table.removeRow(row)


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
        database = Database(db_path)  # Erstelle ein Database-Objekt
        product_list = ProductList(database)  # Übergebe das Database-Objekt an die ProductList-Klasse
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
    
    def update_product_buttons(self):
        for i, product in enumerate(self.vending_machine.get_products()):
            button = self.product_buttons[i]
            button.setText(str(product))
            button.clicked.disconnect()
            button.clicked.connect(lambda _, p=product: self.select_product(p))

    def show_config_dialog(self):
        dialog = ConfigDialog(self, transaction_log=self.vending_machine.transaction_log, product_list=self.vending_machine.product_list)
        if dialog.exec_() == QDialog.Accepted:
            new_products = dialog.get_products()
            self.vending_machine.product_list.save_products(new_products)
            self.refresh_product_buttons()


    def refresh_product_buttons(self):
        # Löschen Sie alle Produkt-Buttons und entfernen Sie sie aus dem Layout
        for button in self.product_buttons:
            button.deleteLater()
            button.setParent(None)

        self.product_buttons = []

        # Erstellen Sie neue Produkt-Buttons und fügen Sie sie zum Layout hinzu
        for i, product in enumerate(self.vending_machine.get_products()):
            button = QPushButton(str(product))
            button.clicked.connect(lambda _, p=product: self.select_product(p))
            self.product_buttons.append(button)
            self.layout().addWidget(button, i // 3, i % 3)

        # Verschieben Sie die restlichen Widgets (coin_button, config_button, buy_button, coin_label, status_label)
        row = len(self.product_buttons) // 3 + 1
        self.layout().addWidget(self.coin_button, row, 0)
        self.layout().addWidget(self.config_button, row, 1)
        self.layout().addWidget(self.buy_button, row, 2)
        self.layout().addWidget(self.coin_label, row + 1, 0)
        self.layout().addWidget(self.status_label, row + 1, 1, 1, 2)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VendingMachineGUI()
    gui.show()
    sys.exit(app.exec_())
