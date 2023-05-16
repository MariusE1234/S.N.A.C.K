#File-imports
from layer2.core_functions import TransactionLog, ProductList, CoinManager, ProductManager, TransactionManager, SalesCalculator
from layer2.validator import DefaultProductValidator
from layer2.vending_machine import VendingMachine
#libraries-imports
import unittest
from unittest.mock import Mock

class TestTransactionLog(unittest.TestCase):
    def setUp(self):
        self.data_access = Mock()
        self.log = TransactionLog(self.data_access)

    def tearDown(self):
        self.data_access.reset_mock()

    def test_add_transaction(self):
        transaction = Mock()
        self.log.add_transaction(transaction)
        self.data_access.add_transaction.assert_called_once_with(transaction, transaction.remaining_stock)

    def test_get_transactions(self):
        self.assertEqual(self.log.get_transactions(), self.data_access.get_transactions())


class TestProductList(unittest.TestCase):
    def setUp(self):
        self.data_access = Mock()
        self.product_list = ProductList(self.data_access)
    
    def tearDown(self):
        self.data_access.reset_mock()

    def test_delete_products(self):
        self.product_list.delete_products()
        self.data_access.clear_products.assert_called_once()

    def test_save_products(self):
        products = [Mock(), Mock()]
        self.product_list.save_products(products)
        self.data_access.save_products.assert_called_once_with(products)
        self.assertEqual(self.product_list.products, products)

    def test_get_products(self):
        self.assertEqual(self.product_list.get_products(), self.data_access.get_products())


class TestCoinManager(unittest.TestCase):
    def setUp(self):
        self.coin_manager = CoinManager()
    
    def tearDown(self):
        self.coin_manager = None

    def test_add_coin(self):
        coin = Mock()
        self.coin_manager.add_coin(coin)
        self.assertIn(coin, self.coin_manager.coins)

    def test_get_total_amount(self):
        coins = [Mock(value=1), Mock(value=2)]
        self.coin_manager.coins = coins
        self.assertEqual(self.coin_manager.get_total_amount(), 3)

    def test_sub_coin(self):
        coins = [Mock(value=1), Mock(value=2)]
        self.coin_manager.coins = coins
        self.assertRaises(ValueError, self.coin_manager.sub_coin, 4)
        self.coin_manager.sub_coin(1)
        self.assertEqual(self.coin_manager.get_total_amount(), 2)


class TestProductManager(unittest.TestCase):
    def setUp(self):
        self.product_manager = ProductManager()
    
    def tearDown(self):
        self.product_manager = None

    def test_select_product(self):
        product = Mock()
        self.product_manager.select_product(product)
        self.assertEqual(self.product_manager.selected_product, product)

    def test_update_stock(self):
        product_list = Mock()
        product = Mock(stock=5)
        self.product_manager.select_product(product)
        self.product_manager.update_stock(product_list)
        product_list.delete_products.assert_called_once()
        product_list.save_products.assert_called_once_with(product_list.products)
        self.assertEqual(self.product_manager.selected_product.stock, 4)

    def test_reset_selected_product(self):
        product = Mock()
        self.product_manager.select_product(product)
        self.product_manager.reset_selected_product()
        self.assertIsNone(self.product_manager.selected_product)


class TestTransactionManager(unittest.TestCase):
    def setUp(self):
        self.transaction_log = Mock()
        self.transaction_manager = TransactionManager(self.transaction_log)
    
    def tearDown(self):
        self.transaction_log.reset_mock()

    def test_add_transaction(self):
        product = Mock(stock=5)
        self.transaction_manager.add_transaction(product)
        self.transaction_log.add_transaction.assert_called_once()

    def test_get_transactions(self):
        self.assertEqual(self.transaction_manager.get_transactions(), self.transaction_log.get_transactions())


class TestSalesCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = SalesCalculator()
    
    def tearDown(self):
        self.calculator = None

    def test_get_total_sales(self):
        transactions = [Mock(amount_paid=5), Mock(amount_paid=10)]
        self.assertEqual(self.calculator.get_total_sales(transactions), 15)

    def test_get_sold_products(self):
        transactions = [Mock(), Mock(), Mock()]
        self.assertEqual(self.calculator.get_sold_products(transactions), 3)

class TestDefaultProductValidator(unittest.TestCase):
    def test_is_valid_name(self):
        test_cases = [
            # Leerzeichen sollten als ungültig behandelt werden
            ("", [], None, (False, "Der Produktname darf nicht leer sein.")),
            # Name bereits vorhanden und aktuelles Produkt ist None
            ("Apfel", ["Apfel", "Birne"], None, (False, "Der Produktname ist bereits vorhanden.")),
            # Name bereits vorhanden, aber aktuelles Produkt hat denselben Namen
            ("Apfel", ["Apfel", "Birne"], Mock(name="Apfel"), (False, "Der Produktname ist bereits vorhanden.")),
            # Gültiger Name, der nicht bereits vorhanden ist
            ("Kirsche", ["Apfel", "Birne"], None, (True, "")),
        ]

        for name, existing_names, current_product, expected in test_cases:
            result = DefaultProductValidator.is_valid_name(name, existing_names, current_product)
            self.assertEqual(result, expected)

    def test_is_valid_image_path(self):
        test_cases = [
            # Leerzeichen sollten als ungültig behandelt werden
            ("", (False, "Ein Bild muss ausgewählt werden.")),
            # Ein Bildpfad sollte als gültig behandelt werden
            ("path/to/image.jpg", (True, "")),
        ]

        for image_path, expected in test_cases:
            result = DefaultProductValidator.is_valid_image_path(image_path)
            self.assertEqual(result, expected)


class TestVendingMachine(unittest.TestCase):
    def setUp(self):
        self.product_list = Mock()
        self.coin_manager = Mock()
        self.transaction_manager = Mock()
        self.product_manager = Mock()  # Create a mock ProductManager
        self.vending_machine = VendingMachine(self.product_list, self.coin_manager, self.transaction_manager)
        self.vending_machine.product_manager = self.product_manager  # Replace the ProductManager instance with the mock
    
    def tearDown(self):
        self.product_list.reset_mock()
        self.coin_manager.reset_mock()
        self.transaction_manager.reset_mock()
        self.product_manager.reset_mock()

    def test_select_product(self):
        product = Mock()
        self.vending_machine.select_product(product)
        self.product_manager.select_product.assert_called_once_with(product)

    def test_buy_product(self):
        # No product selected
        self.product_manager.get_selected_product.return_value = None
        self.assertEqual(self.vending_machine.buy_product(), "Bitte wählen Sie ein Produkt aus.")
        
        # Nicht genug Geld eingeworfen
        product = Mock(price=10)
        self.product_manager.get_selected_product.return_value = product
        self.coin_manager.get_total_amount.return_value = 5
        self.assertEqual(self.vending_machine.buy_product(), "Sie haben nicht genug Geld eingeworfen.")

        # Produkt nicht auf Lager
        self.coin_manager.get_total_amount.return_value = 10 
        product.stock = 0
        self.assertEqual(self.vending_machine.buy_product(), "Dieses Produkt ist leider nicht mehr vorrätig.")

        # Erfolgreicher Kauf
        product.stock = 1
        product.name = "Produkt"
        self.coin_manager.get_total_amount.return_value = 10
        self.assertEqual(self.vending_machine.buy_product(), "Vielen Dank für Ihren Einkauf: Produkt")
        self.transaction_manager.add_transaction.assert_called_once_with(product)
        self.coin_manager.sub_coin.assert_called_once_with(product.price)
        self.vending_machine.product_manager.update_stock.assert_called_once_with(self.product_list)
        self.vending_machine.product_manager.reset_selected_product.assert_called_once()

    def test_get_products(self):
        self.vending_machine.get_products()
        self.product_manager.get_products.assert_called_once_with(self.product_list)


if __name__ == '__main__':
    unittest.main()

