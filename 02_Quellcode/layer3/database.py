#Datei database.py
#File-imports
from layer2.interfaces import IDatabase, IProductDataAccess, ITransactionDataAccess, IConfigDataAccess
#libraries-imports
import sqlite3

db_path = "03_SQL//database//vendingMachine.db"


class Database(IDatabase):
    _instance = None

    def __new__(cls,product_data_access: IProductDataAccess, transaction_data_access: ITransactionDataAccess, config_data_access: IConfigDataAccess):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, product_data_access: IProductDataAccess, transaction_data_access: ITransactionDataAccess, config_data_access: IConfigDataAccess):
        if self.__initialized: return
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        self.product_data_access = product_data_access
        self.transaction_data_access = transaction_data_access
        self.config_data_access = config_data_access
        self.config_data_access.set_default_config()
        self.__initialized = True

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



