# import sqlite3

# def create_connection():
#     conn = sqlite3.connect("inventory.db", check_same_thread=False)
#     return conn


# def create_tables():
#     conn = create_connection()
#     cursor = conn.cursor()

#     # Products table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS products (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         sku TEXT,
#         category TEXT,
#         unit TEXT,
#         stock INTEGER
#     )
#     """)

#     # Transactions table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS transactions (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         product_id INTEGER,
#         type TEXT,
#         quantity INTEGER,
#         date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
#     """)

#     conn.commit()
#     conn.close()


# create_tables()

import sqlite3


def create_connection():
    conn = sqlite3.connect("inventory.db", check_same_thread=False)
    return conn


def create_tables():

    conn = create_connection()
    cursor = conn.cursor()

    # PRODUCTS TABLE
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS products (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     name TEXT,
    #     sku TEXT,
    #     category TEXT,
    #     unit TEXT,
    #     stock INTEGER
    # )
    # """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        sku TEXT,
        category TEXT,
        unit TEXT,
        stock INTEGER,
        location TEXT
    )
    """)

    # TRANSACTIONS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        type TEXT,
        quantity INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # USER TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


# Run table creation
create_tables()