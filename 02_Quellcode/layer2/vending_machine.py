#File-imports
from layer1.entities import Transaction
from layer2.interfaces import IDataAccess, IProductList, ITransactionLog
from layer2.core_functions import TransactionLog

class VendingMachine:
    def __init__(
        self,
        product_list: IProductList,
        coin_slot,
        data_access: IDataAccess,
        transaction_log: ITransactionLog
    ):  # Dependency Injection
        self.product_list = product_list
        self.coin_slot = coin_slot
        self.data_access = data_access
        self.transaction_log = transaction_log
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
