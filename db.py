import sqlite3


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS
        products (
            product_id TEXT UNIQUE NOT NULL,
            product_name TEXT NOT NULL,
            customer TEXT NOT NULL,
            seller TEXT NOT NULL,
            cost_price NUMERIC NOT NULL,
            selling_price NUMERIC NOT NULL
        );
        """)
        self.conn.commit()

    def fetch_all_rows(self):
        self.cur.execute(
            """SELECT product_id, product_name, customer, seller, cost_price, selling_price FROM products""")
        rows = self.cur.fetchall()
        return rows

    def fetch_by_rowid(self, rowid):
        self.cur.execute(
            "SELECT rowid, product_id, product_name, customer, seller, cost_price, selling_price FROM products WHERE rowid=?", (rowid,))
        row = self.cur.fetchall()
        return row

    def fetch_by_product_id(self, product_id):
        self.cur.execute(
            "SELECT rowid, product_id, product_name, customer, seller, cost_price, selling_price FROM products WHERE product_id=?", (product_id,))
        row = self.cur.fetchall()
        return row

    def insert(self, product_id, product_name, customer, seller, cost_price, selling_price):
        self.cur.execute("""INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)""",
                         (product_id, product_name, customer, seller, cost_price, selling_price))
        self.conn.commit()

    def remove(self, product_id):
        self.cur.execute(
            "DELETE FROM products WHERE product_id=?", (product_id, ))
        self.conn.commit()

    def update(self, rowid, product_id, product_name, customer, seller, cost_price, selling_price):
        self.cur.execute("""UPDATE products SET
            product_id=?,
            product_name=?,
            customer=?,
            seller=?,
            cost_price=?,
            selling_price=?
        WHERE
            rowid=?
        """, (product_id, product_name, customer, seller, cost_price, selling_price, rowid))
        self.conn.commit()

    # Defining a destructor to close connections
    def __del__(self):
        self.conn.close()


# db = Database("store.db")

# db.insert("AX2", "4GB DDR4 Ram", "John Doe", "Microcenter", "160", "32.2")
# db.insert("WE12", "Asus Mobo", "Mike Henry", "Microcenter", "360", "345")
# db.insert("FES2", "500w PSU", "Karen Johnson", "Newegg", "80", "453.2")
# db.insert("DEW2", "2GB DDR4 Ram", "Karen Johnson", "Newegg", "70", "45")
# db.insert("DEW5", "24in Monitor", "Sam Smith", "Best Buy", "180", "343")
# db.insert("FR23", "NVIDIA RTX 2080", "Albert Kingston", "Newegg", "679", "432")
# db.insert("XSW2", "600w Corsair PSU", "Karen Johnson", "Newegg", "130", "3421")

# print(db.fetch_all_rows())
