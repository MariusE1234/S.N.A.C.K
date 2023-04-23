#Datei vending_machine.py
#File-imports
from layer2.interfaces import IProductList, ITransactionLog
from layer2.core_functions import ProductManager, TransactionManager

class VendingMachine:
    def __init__(
        self,
        product_list: IProductList,
        coin_slot,
        transaction_log: ITransactionLog
    ):  # Dependency Injection
        self.product_manager = ProductManager(product_list)
        self.transaction_manager = TransactionManager(coin_slot, transaction_log)

    def select_product(self, product):
        self.product_manager.select_product(product)

    def buy_product(self):
        selected_product = self.product_manager.selected_product
        if selected_product is None:
            return "Bitte wählen Sie ein Produkt aus."
        if selected_product.price > self.transaction_manager.coin_slot.get_total_amount():
            return "Sie haben nicht genug Geld eingeworfen."
        if selected_product.stock <= 0:
            return "Dieses Produkt ist leider nicht mehr vorrätig."

        self.transaction_manager.buy_product(selected_product)
        self.product_manager.update_stock()
        self.product_manager.selected_product = None

        return f"Vielen Dank für Ihren Einkauf: {selected_product.name}"

    def get_products(self):
        return self.product_manager.get_products()
