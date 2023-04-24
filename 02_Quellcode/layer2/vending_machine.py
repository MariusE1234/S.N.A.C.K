#Datei vending_machine.py
#File-imports
from layer2.interfaces import IProductList
from layer2.core_functions import ProductManager

class VendingMachine:
    def __init__(
        self,
        product_list: IProductList,
        coinmanager,
        transactionmanager
    ):  # Dependency Injection
        self.productList = product_list
        self.product_manager = ProductManager()
        self.coinmanager = coinmanager
        self.transaction_manager = transactionmanager

    def select_product(self, product):
        self.product_manager.select_product(product)

    def buy_product(self):
        selected_product = self.product_manager.get_selected_product()
        if selected_product is None:
            return "Bitte wählen Sie ein Produkt aus."
        if selected_product.price > self.coinmanager.get_total_amount():
            return "Sie haben nicht genug Geld eingeworfen."
        if selected_product.stock <= 0:
            return "Dieses Produkt ist leider nicht mehr vorrätig."

        self.transaction_manager.add_transaction(selected_product)
        self.coinmanager.sub_coin(selected_product.price)
        self.product_manager.update_stock(self.productList)
        self.product_manager.reset_selected_product()

        return f"Vielen Dank für Ihren Einkauf: {selected_product.name}"

    def get_products(self):
        return self.product_manager.get_products(self.productList)
