import sqlite3

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect('C://Users//Marius//Documents//GitHub//S.N.A.C.K//03_SQL//database//vendingMachine.db')

# Erstelle eine Tabelle products mit Name als PRIMARY KEY und Preis
conn.execute('''CREATE TABLE IF NOT EXISTS products
             (name TEXT PRIMARY KEY,
              price REAL NOT NULL)''')

# Einfügen eines Testdatensatzes
conn.execute("INSERT INTO products (name, price) VALUES ('Cola', 2.0)")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()