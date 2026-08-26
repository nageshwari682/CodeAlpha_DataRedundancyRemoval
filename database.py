import sqlite3

def init_db():
    conn = sqlite3.connect('records.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            record_hash TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def get_all_records():
    conn = sqlite3.connect('records.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM records")
    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_record(name, email, record_hash):
    conn = sqlite3.connect('records.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO records (name, email, record_hash) VALUES (?, ?, ?)",
        (name, email, record_hash)
    )
    conn.commit()
    conn.close()