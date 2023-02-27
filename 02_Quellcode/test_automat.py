
import tkinter as tk

class Assortment:
    def __init__(self):
        self.inventory = {
            "Chips": {"price": 1.5, "quantity": 10},
            "Schokoriegel": {"price": 1.0, "quantity": 15},
            "Cola": {"price": 2.0, "quantity": 8},
            "Wasser": {"price": 1.0, "quantity": 12}
        }
    
    def get_item_price(self, item):
        return self.inventory[item]["price"]
    
    def get_item_quantity(self, item):
        return self.inventory[item]["quantity"]
    
    def set_item_price(self, item, price):
        self.inventory[item]["price"] = price
    
    def set_item_quantity(self, item, quantity):
        self.inventory[item]["quantity"] = quantity
    
    def add_item(self, item, price, quantity):
        self.inventory[item] = {"price": price, "quantity": quantity}
    
    def remove_item(self, item):
        del self.inventory[item]


class VendingMachine:
    def __init__(self):
        self.credit = 0.0
        
    def changeCredit(self, amount):
        self.credit += amount

    def getCredit(self):
        return self.credit


class VendingMachineGUI:
    def __init__(self, vending_machine):
        self.root = tk.Tk()
        self.root.title("Verkaufsautomat")
        self.vm = vending_machine
        
        
        # Erstelle die Buttons für die Artikel
        self.buttons = []
        for row in range(5):
            for col in range(3):
                i = row * 3 + col + 1
                button = tk.Button(self.root, text=f"Artikel {i}")
                button.grid(row=row, column=col, padx=5, pady=5)
                self.buttons.append(button)
        
        # Erstelle das Label für den Preis
        credit_label = tk.Label(self.root, text="Guthaben: {:.2f} Euro".format(vm.getCredit()))
        credit_label.grid(row=0, column=3, sticky="E", padx=5, pady=5)
        
        # Erstelle den Button für das Geldeinwerfen
        insert_money_button = tk.Button(self.root, text="Geld einwerfen", command=self.open_coin_window)
        insert_money_button.grid(row=1, column=3, sticky="E", padx=5, pady=5)
        
        # Erstelle den Button für das Konfigurationsmenü
        config_button = tk.Button(self.root, text="Konfigurationsmenü")
        config_button.grid(row=2, column=3, sticky="E", padx=5, pady=5)
        
        # Erstelle das Label für das Ausgabefach
        output_label = tk.Label(self.root, text="Ausgabefach")
        output_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="W")
        
    def updateLabel(self):
        self.credit_label.configure(text="Guthaben: {:.2f} Euro".format(vm.getCredit()))

    def open_coin_window(self):
        coin_window = tk.Toplevel(self.root)
        
        # Erstelle die Buttons für die Münzen
        coins = [("2 Euro", 2.0), ("1 Euro", 1.0), ("50 Cent", 0.5), 
                 ("20 Cent", 0.2), ("10 Cent", 0.1), ("5 Cent", 0.05), 
                 ("2 Cent", 0.02), ("1 Cent", 0.01)]
        
        for i, (text, amount) in enumerate(coins):
            button = tk.Button(coin_window, text=text, command=lambda amount=amount: vm.changeCredit(amount) update=self.updateLabel())
            button.grid(row=i//4, column=i%4, padx=5, pady=5)
    


    def run(self):
        self.root.mainloop()


class MoneyInputGUI:
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine
        
        # Erstelle das Fenster und den Titel
        self.root = tk.Tk()
        self.root.title("Geld einwerfen")
        
        # Erstelle die Buttons für die Münzen
        coins = [("2 Euro", 2.0), ("1 Euro", 1.0), ("50 Cent", 0.5), 
                 ("20 Cent", 0.2), ("10 Cent", 0.1), ("5 Cent", 0.05), 
                 ("2 Cent", 0.02), ("1 Cent", 0.01)]
        
        for i, (text, amount) in enumerate(coins):
            button = tk.Button(self.root, text=text, command=lambda amount=amount: self.insert_money(amount))
            button.grid(row=i//4, column=i%4, padx=5, pady=5)
    
    def insert_money(self, amount):
        self.vending_machine.changeCredit(amount)
    
    def run(self):
        self.root.mainloop()





vm = VendingMachine()
gui = VendingMachineGUI(vm)



# Zeige das Fenster an
gui.run()