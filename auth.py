# import sqlite3

# def register_user(username, password):

#     conn = sqlite3.connect("inventory.db")
#     cursor = conn.cursor()

#     cursor.execute(
#     "INSERT INTO users (username, password) VALUES (?, ?)",
#     (username, password)
#     )

#     conn.commit()
#     conn.close()


# def login_user(username, password):

#     conn = sqlite3.connect("inventory.db")
#     cursor = conn.cursor()

#     cursor.execute(
#     "SELECT * FROM users WHERE username=? AND password=?",
#     (username, password)
#     )

#     user = cursor.fetchone()

#     conn.close()

#     return user

import sqlite3

def get_connection():
    return sqlite3.connect("inventory.db")

def register_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()
    conn.close()


def login_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user

