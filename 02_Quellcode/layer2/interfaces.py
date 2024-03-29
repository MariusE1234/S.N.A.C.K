#Datei interfaces.py
#libraries-imports
from abc import ABC, abstractmethod

class IDatabase(ABC):
    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def get_ProductDataAccess(self):
        pass
    
    @abstractmethod
    def get_TransactionDataAccess(self):
        pass

    @abstractmethod
    def get_ConfigDataAccess(self):
        pass

class IProductDataAccess(ABC):
    @abstractmethod
    def delete_product(self, product_name):
        pass

    @abstractmethod
    def add_product(self, product):
        pass

    @abstractmethod
    def get_products(self):
        pass

    @abstractmethod
    def update_product(self, old_product, new_product):
        pass

    @abstractmethod
    def save_products(self, products):
        pass

    @abstractmethod
    def clear_products(self):
        pass

    @abstractmethod
    def update_product_image_path(self, product_name, image_path):
        pass

    @abstractmethod
    def get_product_image_path(self, product_name):
        pass

class ITransactionDataAccess(ABC):
    @abstractmethod
    def add_transaction(self, transaction, remaining_stock):
        pass

    @abstractmethod
    def get_transactions(self):
        pass

class IConfigDataAccess(ABC):
    @abstractmethod
    def set_default_config(self):
        pass

    @abstractmethod
    def get_config(self, key):
        pass

    @abstractmethod
    def update_config(self, key, value):
        pass

class ITransactionLog(ABC):
    @abstractmethod
    def add_transaction(self, transaction):
        pass

    @abstractmethod
    def get_transactions(self):
        pass

class IProductList(ABC):
    @abstractmethod
    def save_products(self, products):
        pass

    @abstractmethod
    def delete_products(self):
        pass

    @abstractmethod
    def get_products(self):
        pass

class IProductValidator(ABC):
    @staticmethod
    @abstractmethod
    def is_valid_name(name, existing_names, current_product=None):
        pass

    @staticmethod
    @abstractmethod
    def is_valid_image_path(image_path):
        pass