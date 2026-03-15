import sqlite3, os
conn = sqlite3.connect('data/website.db')
conn.executescript('''
    CREATE TABLE IF NOT EXISTS "order" (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id       INT,
        user_email    VARCHAR(200),
        user_address  VARCHAR(200),
        user_mobile   INT,
        purchase_date DATE,
        ship_date     DATE,
        status        INT DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS order_details (
        order_id      INT,
        product_id    INT,
        price         NUMERIC,
        quantity      INT,
        purchase_date DATE,
        FOREIGN KEY (order_id) REFERENCES "order"(id)
    );
''')

conn.commit()
conn.close()
print(" Tạo bảng order và order_details thành công!")