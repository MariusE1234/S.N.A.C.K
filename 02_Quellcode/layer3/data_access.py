#Datei data_access.py
#File-imports
from layer1.entities import Transaction, Product
from layer2.interfaces import IProductDataAccess, ITransactionDataAccess, IConfigDataAccess
#libraries-imports
import datetime
from sqlite3 import Error

class ProductDataAccess(IProductDataAccess):
    def __init__(self, conn):
        self.conn = conn

    def delete_product(self, product_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM products WHERE name = ?", (product_name,))
            self.conn.commit()
        except Error as e:
            print(e)

    def add_product(self, product):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO products (name, price, stock, image_path) VALUES (?, ?, ?, ?)", (product.name, product.price, product.stock, product.image_path))
            self.conn.commit()
        except Error as e:
            print(e)

    def get_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, price, stock, image_path FROM products")
        rows = cursor.fetchall()

        products = [Product(row[0], row[1], row[2], row[3]) for row in rows]
        return products

    def update_product(self, old_product, new_product):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE products SET name = ?, price = ?, stock = ?, image_path = ? WHERE name = ?", (new_product.name, new_product.price, new_product.stock, new_product.image_path, old_product.name))
            self.conn.commit()
        except Error as e:
            print(e)

    def save_products(self, products):
        try:
            cursor = self.conn.cursor()
            for product in products:
                # Prüfen, ob ein Produkt mit demselben Namen bereits in der Datenbank vorhanden ist
                cursor.execute("SELECT COUNT(*) FROM products WHERE name=?", (product.name,))
                count = cursor.fetchone()[0]

                if count == 0:
                    # Fügen Sie das Produkt hinzu, wenn es noch nicht in der Datenbank vorhanden ist
                    cursor.execute("INSERT INTO products (name, price, stock, image_path) VALUES (?, ?, ?, ?)",            (product.name, product.price, product.stock, product.image_path))
                else:
                    # Aktualisieren Sie den Eintrag, wenn das Produkt bereits in der Datenbank vorhanden ist
                    cursor.execute("UPDATE products SET price=?, stock=?, image_path=? WHERE name=?", (product.price, product.stock, product.image_path, product.name))
            self.conn.commit()
        except Error as e:
         print(e)

    def clear_products(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM products")
            self.conn.commit()
        except Error as e:
            print(e)

    def update_product_image_path(self, product_name, image_path):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE products SET image_path = ? WHERE name = ?", (image_path, product_name))
            self.conn.commit()
        except Error as e:
            print(e)

    def get_product_image_path(self, product_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT image_path FROM products WHERE name = ?", (product_name,))
        row = cursor.fetchone()
        return row[0] if row else None

class TransactionDataAccess(ITransactionDataAccess):
    def __init__(self, conn):
        self.conn = conn

    def add_transaction(self, transaction, remaining_stock):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO transactions (product_name, price, remaining_stock, datetime) VALUES (?, ?, ?, ?)", (transaction.product_name, transaction.amount_paid, remaining_stock, transaction.timestamp.strftime("%Y-%m-%d %H:%M:%S")))
            self.conn.commit()
        except Error as e:
            print(e)

    def get_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT product_name, price, remaining_stock, datetime FROM transactions")
        rows = cursor.fetchall()
        transactions = [Transaction(row[0], row[1], row[2], datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")) for row in rows]
        return transactions

class ConfigDataAccess(IConfigDataAccess):
    def __init__(self, conn):
        self.conn = conn

    def set_default_config(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM config WHERE key=?", ("pin",))
        pin = cursor.fetchone()

        if pin is None:
            cursor.execute("INSERT INTO config (key, value) VALUES (?, ?)", ("pin", "1111"))
            self.conn.commit()

    def get_config(self, key):
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM config WHERE key=?", (key,))
        value = cursor.fetchone()
        return value[0] if value else None

    def update_config(self, key, value):
        self.conn.execute("UPDATE config SET value=? WHERE key=?", (value, key))
        self.conn.commit()
