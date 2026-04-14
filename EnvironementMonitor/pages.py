from flask import Blueprint, render_template, request, jsonify
from TemperatureDB import TemperatureDB
from temp_reading import read_temperature, Temperature
from humidity_reading import read_humidity
from air_quality_reading import read_air_quality
from AirQualityDB import AirQualityDB
from HumidityDB import HumidityDB
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

bp = Blueprint('pages', __name__)

@bp.route('/')
def home():
    return render_template('pages/home.html') 

@bp.route('/about')
def about():
    return render_template('pages/about.html')

@bp.route('/api/temperature', methods=['GET'])
def get_temperature():
    temperature = read_temperature()
    temperature_db = TemperatureDB()
    temperature_db.insert_temperature(temperature)
    temperature_db.close()

    return jsonify({
        "temperature": temperature.get_value(),
        "unit": "°C",
        "timestamp": temperature.get_timestamp()
    })

@bp.route('/api/humidity', methods=['GET'])
def get_humidity():
    humidity = read_humidity()
    humidity_db = HumidityDB()
    humidity_db.insert_humidity(humidity)
    humidity_db.close()

    return jsonify({
        "humidity": humidity.get_value(),
        "unit": "%",
        "timestamp": humidity.get_timestamp()
    })


@bp.route('/api/air-quality', methods=['GET'])
def get_air_quality():
    air_quality = read_air_quality()
    air_quality_db = AirQualityDB()
    air_quality_db.insert_air_quality(air_quality)
    air_quality_db.close()
    return jsonify({
        "iaq": air_quality.get_iaq(),
        "raw": air_quality.get_raw(),
        "temperature": air_quality.get_temperature(),
        "humidity": air_quality.get_humidity(),
        "timestamp": air_quality.get_timestamp(),
        "warming": air_quality.is_warming_up(),
        "unit": "IAQ"
    })


@bp.route('/air-quality-by-date', methods=['GET'])
def air_quality_by_date():
    timestamp = request.args.get('timestamp')
    air_quality_db = AirQualityDB()

    if not timestamp:
        return jsonify({"error": "timestamp is required"}), 400

    try:
        date_str, rows = air_quality_db.get_air_quality_by_date_from_timestamp(timestamp)
    except ValueError:
        return jsonify({"error": "Invalid timestamp"}), 400

    air_quality_db.close()

    if not rows:
        return jsonify({"message": f"No data for {date_str}"}), 404

    times = []
    for row in rows:
        ts = row[1]
        if isinstance(ts, (int, float)):
            times.append(datetime.fromtimestamp(ts))
        else:
            times.append(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"))
    iaqs = [row[0] for row in rows]

    plt.figure(figsize=(10, 5))
    plt.plot(times, iaqs, marker='o')
    plt.xlabel("Time")
    plt.ylabel("Air Quality Index")
    plt.title(f"Air Quality Index on {date_str}")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return jsonify({
        "date": date_str,
        "graph": image_base64
    })


@bp.route('/gas-value-by-date', methods=['GET'])
def gas_value_by_date():
    timestamp = request.args.get('timestamp')
    air_quality_db = AirQualityDB()

    if not timestamp:
        return jsonify({"error": "timestamp is required"}), 400

    try:
        date_str, rows = air_quality_db.get_raw_by_date_from_timestamp(timestamp)
    except ValueError:
        return jsonify({"error": "Invalid timestamp"}), 400

    air_quality_db.close()

    if not rows:
        return jsonify({"message": f"No data for {date_str}"}), 404

    times = []
    for row in rows:
        ts = row[1]
        if isinstance(ts, (int, float)):
            times.append(datetime.fromtimestamp(ts))
        else:
            times.append(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"))
    raw_values = [row[0] for row in rows]

    plt.figure(figsize=(10, 5))
    plt.plot(times, raw_values, marker='o')
    plt.xlabel("Time")
    plt.ylabel("Raw Gas Value")
    plt.title(f"Raw Gas Value on {date_str}")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return jsonify({
        "date": date_str,
        "graph": image_base64
    })


@bp.route('/humidity-by-date', methods=['GET'])
def humidity_by_date():
    timestamp = request.args.get('timestamp')
    humiditydb = HumidityDB()

    if not timestamp:
        return jsonify({"error": "timestamp is required"}), 400

    try:
        date_str, rows = humiditydb.get_humidity_by_date_from_timestamp(timestamp)
    except ValueError:
        return jsonify({"error": "Invalid timestamp"}), 400

    humiditydb.close()

    if not rows:
        return jsonify({"message": f"No data for {date_str}"}), 404

    times = []
    for row in rows:
        ts = row[1]
        if isinstance(ts, (int, float)):
            times.append(datetime.fromtimestamp(ts))
        else:
            times.append(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"))
    humidity_values = [row[0] for row in rows]

    plt.figure(figsize=(10, 5))
    plt.plot(times, humidity_values, marker='o')
    plt.xlabel("Time")
    plt.ylabel("Humidity (%)")
    plt.title(f"Humidity on {date_str}")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return jsonify({
        "date": date_str,
        "graph": image_base64
    })


@bp.route('/temperature-by-date', methods=['GET'])
def temperature_by_date():
    timestamp = request.args.get('timestamp')
    temperaturedb = TemperatureDB()

    if not timestamp:
        return jsonify({"error": "timestamp is required"}), 400

    try:
        date_str, rows = temperaturedb.get_temperatures_by_date_from_timestamp(timestamp)
    except ValueError:
        return jsonify({"error": "Invalid timestamp"}), 400

    if not rows:
        return jsonify({"message": f"No data for {date_str}"}), 404

    # Extract data

    times = []
    for row in rows:
        ts = row[1]

        if isinstance(ts, (int, float)):
            times.append(datetime.fromtimestamp(ts))
        else:
            times.append(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"))
   
    # times = [datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S") for row in rows]
    temps = [row[0] for row in rows]

    # Plot graph
    plt.figure(figsize=(10, 5))
    plt.plot(times, temps, marker='o')
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title(f"Temperature on {date_str}")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xticks(rotation=45)
    plt.grid(True)

    plt.tight_layout()

    # Convert to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return jsonify({
        "date": date_str,
        "graph": image_base64
    })