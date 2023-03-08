import tkinter as tk
from tkinter import messagebox

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class VendingMachine:
    def __init__(self):
        self.products = [Product("Chips", 1.50), Product("Cola", 2.00), Product("Water", 1.00), Product("M&M`s", 1.00)]
        self.balance = 0.0

    def insert_coin(self, amount):
        self.balance += amount

    def get_product(self, index):
        if index >= 0 and index < len(self.products):
            product = self.products[index]
            if self.balance >= product.price:
                self.balance -= product.price
                return product
        return None

class VendingMachineGUI:
    def __init__(self):
        self.vending_machine = VendingMachine()

        self.root = tk.Tk()
        self.root.title("Vending Machine")

        self.balance_label = tk.Label(self.root, text="Balance: $0.00")
        self.balance_label.grid(row=0, column=0, columnspan=3)

        for i in range(len(self.vending_machine.products)):
            product = self.vending_machine.products[i]
            button = tk.Button(self.root, text=product.name+"\n"+str(product.price)+"$", command=lambda index=i: self.buy_product(index))
            button.grid(row=i+1, column=1)

        coin_button = tk.Button(self.root, text="Insert Coin", command=self.open_coin_window)
        coin_button.grid(row=len(self.vending_machine.products)+1, column=0)

        config_button = tk.Button(self.root, text="Configuration Menu", command=self.open_config_window)
        config_button.grid(row=len(self.vending_machine.products)+1, column=1)

    def update_balance_label(self):
        self.balance_label.config(text="Balance: $" + str(self.vending_machine.balance))

    def buy_product(self, index):
        product = self.vending_machine.get_product(index)
        if product is not None:
            tk.messagebox.showinfo("Purchase Complete", "You bought a " + product.name)
            self.update_balance_label()
        else:
            tk.messagebox.showerror("Purchase Error", "You don't have enough balance to buy this product")

    def open_coin_window(self):
        coin_window = tk.Toplevel(self.root)
        coin_window.title("Insert Coin")
        coin_window.geometry("200x100")

        coin_label = tk.Label(coin_window, text="Enter amount to insert:")
        coin_label.pack()

        coin_entry = tk.Entry(coin_window)
        coin_entry.pack()

        submit_button = tk.Button(coin_window, text="Submit", command=lambda: self.insert_coin(coin_entry.get(), coin_window))
        submit_button.pack()

    def insert_coin(self, amount_str, window):
        try:
            amount = float(amount_str)
            self.vending_machine.insert_coin(amount)
            self.update_balance_label()
            tk.messagebox.showinfo("Insert Coin", "$" + str(amount) + " inserted")
            window.destroy()
        except ValueError:
            tk.messagebox.showerror("Insert Coin Error", "Invalid amount")

    def open_config_window(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuration Menu")
        config_window.geometry("200x100")

        text_label = tk.Label(config_window, text="Configure the vending machine:")
        text_label.pack()

        reset_button = tk.Button(config_window, text="Reset Balance", command=self.reset_balance)
        reset_button.pack()

    def reset_balance(self):
        self.vending_machine.balance = 0.0
        self.update_balance_label()
        tk.messagebox.showinfo("Reset Balance", "Balance reset to $0.00")

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    gui = VendingMachineGUI()
    gui.run()
