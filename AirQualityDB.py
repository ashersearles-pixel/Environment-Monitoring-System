from air_quality_reading import AirQuality
import sqlite3
from datetime import datetime


class AirQualityDB:
    def __init__(self):
        self.conn = sqlite3.connect("air_quality.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS air_quality_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            iaq INTEGER,
            raw INTEGER,
            temperature REAL,
            humidity REAL,
            timestamp TEXT
        )
        """)
        self.conn.commit()

    def insert_air_quality(self, air_quality: AirQuality):
        self.cursor.execute(
            "INSERT INTO air_quality_log (iaq, raw, temperature, humidity, timestamp) VALUES (?, ?, ?, ?, ?)",
            (
                air_quality.get_iaq(),
                air_quality.get_raw(),
                air_quality.get_temperature(),
                air_quality.get_humidity(),
                air_quality.get_timestamp(),
            ),
        )
        self.conn.commit()

    def get_air_quality_by_date_from_timestamp(self, timestamp):
        if isinstance(timestamp, str) and timestamp.isdigit():
            timestamp = int(timestamp)

        if isinstance(timestamp, (int, float)):
            date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        else:
            try:
                date_str = datetime.strptime(timestamp, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError as e:
                raise ValueError("Invalid timestamp") from e

        like_pattern = f"{date_str}%"
        self.cursor.execute(
            "SELECT iaq, timestamp FROM air_quality_log WHERE timestamp LIKE ? ORDER BY timestamp",
            (like_pattern,),
        )
        rows = self.cursor.fetchall()
        return date_str, rows

    def get_raw_by_date_from_timestamp(self, timestamp):
        if isinstance(timestamp, str) and timestamp.isdigit():
            timestamp = int(timestamp)

        if isinstance(timestamp, (int, float)):
            date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        else:
            try:
                date_str = datetime.strptime(timestamp, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError as e:
                raise ValueError("Invalid timestamp") from e

        like_pattern = f"{date_str}%"
        self.cursor.execute(
            "SELECT raw, timestamp FROM air_quality_log WHERE timestamp LIKE ? ORDER BY timestamp",
            (like_pattern,),
        )
        rows = self.cursor.fetchall()
        return date_str, rows

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = AirQualityDB()
    print("AirQualityDB ready")
    db.close()
