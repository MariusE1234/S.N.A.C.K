import tkinter as tk

class MyGUI:
    def __init__(self, master):
        self.master = master
        self.button = tk.Button(master, text="Weiter", command=self.open_new_window)
        self.button.pack()

    def open_new_window(self):
        new_window = tk.Toplevel(self.master)
        new_button1 = tk.Button(new_window, text="Button 1")
        new_button1.pack()
        new_button2 = tk.Button(new_window, text="Button 2")
        new_button2.pack()

# Erstelle ein neues Tkinter-Fenster
window = tk.Tk()

# Erstelle eine GUI-Instanz
gui = MyGUI(window)

# Zeige das Fenster an
window.mainloop()
