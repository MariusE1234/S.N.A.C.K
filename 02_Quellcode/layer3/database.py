#File-imports
from layer3.data_access import ProductDataAccess, TransactionDataAccess, ConfigDataAccess
#libraries-imports
import sqlite3

db_path = "03_SQL//database//vendingMachine.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        self.product_data_access = ProductDataAccess(self.conn)
        self.transaction_data_access = TransactionDataAccess(self.conn)
        self.config_data_access = ConfigDataAccess(self.conn)
        self.config_data_access.set_default_config()

    def create_tables(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                name TEXT PRIMARY KEY,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                image_path TEXT
            );
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                price REAL NOT NULL,
                remaining_stock INTEGER,
                datetime TEXT NOT NULL
            );
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS config (
                id INTEGER PRIMARY KEY,
                key TEXT NOT NULL UNIQUE,
                value TEXT NOT NULL
            );
            """
        )

    def get_ProductDataAccess(self):
        return self.product_data_access
    
    def get_TransactionDataAccess(self):
        return self.transaction_data_access

    def get_ConfigDataAccess(self):
        return self.config_data_access

