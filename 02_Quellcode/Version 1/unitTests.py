import unittest
from unittest.mock import MagicMock, patch
from vending_machine import *

class TestProduct(unittest.TestCase):
    def test_init(self):
        product = Product("Testprodukt", 1.23)
        self.assertEqual(product.name, "Testprodukt")
        self.assertEqual(product.price, 1.23)

    def test_str(self):
        product = Product("Testprodukt", 1.23)
        self.assertEqual(str(product), "Testprodukt (1.23 €)")

class TestProductList(unittest.TestCase):
    def test_init(self):
        product_list = ProductList()
        self.assertEqual(len(product_list.products), 6)

class TestCoin(unittest.TestCase):
    def test_init(self):
        coin = Coin(1.23)
        self.assertEqual(coin.value, 1.23)

    def test_str(self):
        coin = Coin(1.23)
        self.assertEqual(str(coin), "1.23 €")

class TestCoinSlot(unittest.TestCase):
    def test_init(self):
        coin_slot = CoinSlot()
        self.assertEqual(len(coin_slot.coins), 0)

    def test_add_coin(self):
        coin_slot = CoinSlot()
        coin_slot.add_coin(Coin(1))
        self.assertEqual(len(coin_slot.coins), 1)

    def test_get_total_amount(self):
        coin_slot = CoinSlot()
        coin_slot.add_coin(Coin(0.5))
        coin_slot.add_coin(Coin(0.5))
        self.assertEqual(coin_slot.get_total_amount(), 1)

    def test_reset(self):
        coin_slot = CoinSlot()
        coin_slot.add_coin(Coin(1))
        coin_slot.reset()
        self.assertEqual(len(coin_slot.coins), 0)

class TestVendingMachine(unittest.TestCase):
    def setUp(self):
        self.product_list = ProductList()
        self.vending_machine = VendingMachine()

    def test_select_product(self):
        self.vending_machine.select_product(self.product_list.products[0])
        self.assertEqual(self.vending_machine.selected_product, self.product_list.products[0])

    def test_buy_product_no_product_selected(self):
        message = self.vending_machine.buy_product()
        self.assertEqual(message, "Bitte wählen Sie ein Produkt aus.")

    def test_buy_product_not_enough_money(self):
        self.vending_machine.select_product(self.product_list.products[0])
        self.assertEqual(self.vending_machine.buy_product(), "Sie haben nicht genug Geld eingeworfen.")

    def test_buy_product_successful(self):
        self.vending_machine.select_product(self.product_list.products[0])
        self.vending_machine.coin_slot.add_coin(Coin(2))
        message = self.vending_machine.buy_product()
        self.assertEqual(message, "Vielen Dank für Ihren Einkauf: Cola")
        self.assertEqual(self.vending_machine.selected_product, None)
        self.assertEqual(len(self.vending_machine.coin_slot.coins), 0)

    def test_get_products(self):
        products = self.vending_machine.get_products()
        self.assertEqual(len(products), 6)

class TestCoinsDialog(unittest.TestCase):
    def test_init(self):
        dialog = CoinsDialog()
        self.assertEqual(len(dialog.coins), 6)

    def test_get_products(self):
        dialog = ConfigDialog()
        products = dialog.get_products()
        self.assertEqual(len(products), 6)
        self.assertEqual(products[0].name, "Cola")
        self.assertEqual(products[0].price, 1.5)

class TestVendingMachineGUI(unittest.TestCase):
    def setUp(self):
        self.gui = VendingMachineGUI()

    def test_select_product(self):
        self.gui.select_product(Product("Cola", 1.5))
        self.assertEqual(self.gui.status_label.text(), "Bitte werfen Sie 1.5 € ein.")

    def test_buy_product_no_product_selected(self):
        self.gui.buy_product()
        self.assertEqual(self.gui.status_label.text(), "Bitte wählen Sie ein Produkt aus.")

    def test_buy_product_not_enough_money(self):
        self.gui.select_product(Product("Cola", 1.5))
        self.gui.buy_product()
        self.assertEqual(self.gui.status_label.text(), "Sie haben nicht genug Geld eingeworfen.")

    def test_buy_product_successful(self):
        self.gui.select_product(Product("Cola", 1.5))
        self.gui.vending_machine.coin_slot.add_coin(Coin(2))
        self.gui.buy_product()
        self.assertEqual(self.gui.status_label.text(), "Vielen Dank für Ihren Einkauf: Cola")
        self.assertEqual(len(self.gui.vending_machine.coin_slot.coins), 0)

    def test_show_coin_dialog(self):
        with patch("vending_machine.CoinsDialog") as MockCoinsDialog:
            mock_dialog = MagicMock()
            MockCoinsDialog.return_value = mock_dialog
            mock_dialog.exec_.return_value = QDialog.Accepted
            mock_dialog.selected_coin = Coin(1)
            self.gui.show_coin_dialog()
            self.assertEqual(self.gui.coin_label.text(), "1.0 €")

    def test_show_config_dialog(self):
        with patch("vending_machine.ConfigDialog") as MockConfigDialog:
            mock_dialog = MagicMock()
            MockConfigDialog.return_value = mock_dialog
            mock_dialog.exec_.return_value = QDialog.Accepted
            mock_dialog.get_products.return_value = [Product("Testprodukt", 1.23)]
            self.gui.show_config_dialog()
            self.assertEqual(len(self.gui.vending_machine.product_list.products), 1)
            self.assertEqual(self.gui.vending_machine.product_list.products[0].name, "Testprodukt")
            self.assertEqual(self.gui.vending_machine.product_list.products[0].price, 1.23)

if __name__ == "__main__":
    unittest.main()        
                         
