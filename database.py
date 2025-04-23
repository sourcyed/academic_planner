import sqlite3
from config import DB_NAME
import logging

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                date TEXT,
                priority TEXT,
                category TEXT
            )
        """)
        conn.commit()
        logging.info(f"Database table created.")
    except sqlite3.Error as e:
        logging.error(f"DB Init Error: {e}")
    finally:
        conn.close()


def insert_event(event):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO events (title, date, priority, category)
            VALUES (?, ?, ?, ?)
            """,
            (event['summary'], event['start'], event['priority'], event['category'])
        )
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Insert Error: {e}")
    finally:
        conn.close()


def fetch_events():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events ORDER BY date ASC")
        logging.info(f"Fetched events from the database")
        return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Fetch Error: {e}")
        return []
    finally:
        conn.close()


def fetch_event_counts_per_day():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date(date) as day, COUNT(*) as count
            FROM events
            GROUP BY date(date)
            ORDER BY day ASC
        """)
        logging.info(f"Fetched busy level data from the database")
        return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Busy level fetch error: {e}")
        return []
    finally:
        conn.close()