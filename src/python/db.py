import sqlite3


def create_table(name='user_db.db'):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()

    # Create User table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_active INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_table()
