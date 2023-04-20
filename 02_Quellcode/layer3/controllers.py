#File-imports
from layer1.entities import Product, Coin
from layer2.interfaces import IConfigDataAccess,IProductDataAccess, ITransactionDataAccess, IProductList, ITransactionLog
from layer2.validator import ProductValidator
from layer2.core_functions import SalesCalculator

class ConfigController:
    def __init__(
        self,
        product_list: IProductList = None,
        transaction_data_access: ITransactionDataAccess = None,
        product_data_access: IProductDataAccess = None,
        config_data_access: IConfigDataAccess = None
    ):
        self.product_list = product_list
        self.transaction_data_access = transaction_data_access
        self.product_data_access = product_data_access
        self.config_data_access = config_data_access

    def is_name_unique(self, name, product_table, exclude_row=None):
        for row in range(product_table.rowCount()):
            if row != exclude_row and product_table.item(row, 0).text() == name:
                return False
        return True

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

    def get_products_from_table(self, product_table):
        products = []
        for i in range(product_table.rowCount()):
            name_item = product_table.item(i, 0)
            price_item = product_table.item(i, 1)
            stock_item = product_table.item(i, 2)
            image_item = product_table.item(i, 3)
            if name_item is not None and price_item is not None and stock_item is not None:
                products.append(Product(name_item.text(), float(price_item.text()), int(stock_item.text()),image_item.text()))
        return products

    def update_config(self, value, new_pin):
        self.config_data_access.update_config(value, new_pin)
    
class StatController:
    def __init__(
        self,
        transaction_data_access: ITransactionDataAccess = None
    ):
        self.transaction_data_access = transaction_data_access
        self.salesCalc = SalesCalculator()

    def get_total_sales(self):
        return self.salesCalc.get_total_sales(self.transaction_data_access.get_transactions())
    
    def get_sold_products(self):
        return self.salesCalc.get_sold_products(self.transaction_data_access.get_transactions())