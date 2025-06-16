import sqlite3

# Create connection and table (if not exists)
def init_db():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parent_directories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            status BOOLEAN DEFAULT 0
        );
    """)

    conn.commit()
    conn.close()

# Get connection
def get_connection():
    return sqlite3.connect("test.db")
