#Datei entities.py
#libraries-imports
import datetime

class Transaction:
    def __init__(self, product_name, amount_paid, remaining_stock, timestamp=None):
        self.product_name = product_name
        self.amount_paid = amount_paid
        self.remaining_stock = remaining_stock
        self.timestamp = timestamp if timestamp else datetime.datetime.now()

    def __str__(self):
        formatted_timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")  # Format ohne Nachkommastellen
        return f"{formatted_timestamp} : {self.product_name} {self.amount_paid} € - Verbleibender Bestand: {self.remaining_stock}"

    @classmethod
    def create(cls, product_name, amount_paid, remaining_stock, timestamp=None):
        return cls(product_name, amount_paid, remaining_stock, timestamp)


class Product:
    def __init__(self, name, price, stock, image_path):
        self.name = name
        self.price = price
        self.stock = stock
        self.image_path = image_path

    def __str__(self):
        return f"{self.name} ({self.price} €)"
    
    @classmethod
    def create(cls, name, price, stock, image_path):
        return cls(name, price, stock, image_path)
    
class Coin:
    available_coins = [0.05, 0.1, 0.2, 0.5, 1, 2]

    def __init__(self, value):
        if value in Coin.available_coins:
            self.value = value
        else:
            raise ValueError("Ungültiger Münzwert")

    def __str__(self):
        return f"{self.value} €"
    
    @classmethod
    def get_availableCoins(cls):
        return cls.available_coins