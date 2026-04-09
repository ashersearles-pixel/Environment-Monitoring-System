from humidity_reading import read_humidity
from Humidity import Humidity
import sqlite3
from datetime import datetime
from time import sleep

class HumidityDB:
    def __init__(self):
        # 1. Connect to SQLite DB (creates file if not exists)
        self.conn = sqlite3.connect("humidity.db")
        self.cursor = self.conn.cursor()

        # 2. Create table (only runs once)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS humidity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            humidity REAL,
            timestamp TEXT
        )
        """)
        self.conn.commit()


    def insert_humidity(self, humidity):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO humidity_log (humidity, timestamp) VALUES (?, ?)",
            (humidity.value, humidity.timestamp)
        )
        self.conn.commit()


    def close(self):
        self.conn.close()

if __name__ == "__main__":
    humidity_db = HumidityDB()
    for _ in range(5):
        humidity = read_humidity()
        humidity_db.insert_humidity(humidity)
        print(f"Saved: {humidity} at {datetime.now()}")
        sleep(1)
    

    humidity_db.close()