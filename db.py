
import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Создаем таблицу продуктов
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                                id TEXT PRIMARY KEY,
                                name TEXT,
                                photo BLOB,
                                description TEXT, 
                                price TEXT
                                )''')

        # Создаем таблицу корзины
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Cart (
                                id TEXT PRIMARY KEY,
                                name TEXT, 
                                photo BLOB,
                                description TEXT,
                                price TEXT
                                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Sos (
                                user_id INTEGER PRIMERY KEY,
                                type TEXT,
                                appeal TEXT
                                )''')

        self.conn.commit()

    # добавление товара в Продукты
    def add_product(self, product_id, name, photo, description, price):
        self.cursor.execute('''INSERT INTO Products (id, name, photo, description, price) VALUES (?, ?, ?, ?, ?)''',
                            (product_id, name, sqlite3.Binary(photo), description, price))
        self.conn.commit()

    # выбор товара в Продукты
    def select_product(self, product_id):
        self.cursor.execute('''SELECT * FROM Products WHERE id = ?''', (product_id,))
        return self.cursor.fetchone()

    # добвление товара в Корзину
    def move_to_cart(self, product_id):
        product = self.select_product(product_id)
        if product:
            self.cursor.execute('''INSERT INTO Cart (id, name, photo, description, price) VALUES (?, ?, ?, ?, ?)''',
                                (product_id, product[1], product[2], product[3], product[4]))
            self.cursor.execute('''DELETE FROM Products WHERE id = ?''', (product_id,))
            self.conn.commit()
            return True
        else:
            return False

    # выбрать все товары
    def get_all_products(self):
        self.cursor.execute('''SELECT * FROM Products''')
        return self.cursor.fetchall()

        # Выбор товара из корзины

    def select_product_in_cart(self, product_id):
        self.cursor.execute('''SELECT * FROM Cart WHERE id = ?''', (product_id,))
        return self.cursor.fetchone()

        # Перенос товара из корзины в таблицу Products

    def move_to_products(self, product_id):
        product = self.select_product_in_cart(product_id)
        if product:
            self.cursor.execute('''INSERT INTO Products (id, name, photo, description, price) VALUES (?, ?, ?, ?, ?)''',
                                (product[0], product[1], product[2], product[3], product[4]))
            self.cursor.execute('''DELETE FROM Cart WHERE id = ?''', (product_id,))
            self.conn.commit()
            return True
        else:
            return False

    def get_all_products_in_cart(self):
        self.cursor.execute('''SELECT * FROM Cart''')
        return self.cursor.fetchall()

    # добавить вопрос
    def add_question(self, user_id, type, appeal):
        self.cursor.execute('''INSERT INTO Sos (user_id, type, appeal) VALUES (?, ?, ?)''',
                            (user_id, type, appeal))
        self.conn.commit()

    # выдать все вопросы
    def get_appeals(self):
        self.cursor.execute('''SELECT * FROM Sos''')
        return self.cursor.fetchall()
    def close(self):
        self.conn.close()
