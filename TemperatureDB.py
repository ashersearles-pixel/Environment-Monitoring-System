from temp_reading import read_temperature
from Temperature import Temperature
import sqlite3
from datetime import datetime
from time import sleep

class TemperatureDB:
    def __init__(self):
        # 1. Connect to SQLite DB (creates file if not exists)
        self.conn = sqlite3.connect("temperature.db")
        self.cursor = self.conn.cursor()

        # 2. Create table (only runs once)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperature_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            timestamp TEXT
        )
        """)
        self.conn.commit()


    def insert_temperature(self, temp):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO temperature_log (temperature, timestamp) VALUES (?, ?)",
            (temp.get_temperature(), temp.get_timestamp())
        )
        self.conn.commit()

    def get_temperatures_by_date_from_timestamp(self, timestamp):
        # Accept either an epoch integer or a string timestamp.
        if isinstance(timestamp, str) and timestamp.isdigit():
            timestamp = int(timestamp)

        if isinstance(timestamp, (int, float)):
            date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        else:
            # Allow ISO date strings as fallback
            try:
                date_str = datetime.strptime(timestamp, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError as e:
                raise ValueError("Invalid timestamp") from e

        like_pattern = f"{date_str}%"
        self.cursor.execute(
            "SELECT temperature, timestamp FROM temperature_log WHERE timestamp LIKE ? ORDER BY timestamp",
            (like_pattern,)
        )
        rows = self.cursor.fetchall()
        return date_str, rows

    def get_all_temperatures(self):
        self.cursor.execute("SELECT temperature FROM temperature_log")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    temp_db = TemperatureDB()
    for _ in range(5):
        temp = read_temperature()
        temp_db.insert_temperature(temp)
        print(f"Saved: {temp} at {datetime.now()}")
        sleep(1)
    

    temp_db.close()