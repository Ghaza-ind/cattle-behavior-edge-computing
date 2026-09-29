from flask import Flask, request, jsonify
import mysql.connector
import time

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="cow_behavior"
    )

# ===============================
# API: Terima data dari ESP8266
# ===============================
@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json(force=True)

    if not data:
        return jsonify({"error": "No data"}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Jika data berupa array (batch)
    if isinstance(data, list):

        for item in data:
            cursor.execute("""
                INSERT INTO accelerometer_data (ax, ay, az, gx, gy, gz)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                item['ax'],
                item['ay'],
                item['az'],
                item['gx'],
                item['gy'],
                item['gz']
            ))

    # Jika data hanya 1 object (backup mode)
    else:
        cursor.execute("""
            INSERT INTO accelerometer_data (ax, ay, az, gx, gy, gz)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['ax'],
            data['ay'],
            data['az'],
            data['gx'],
            data['gy'],
            data['gz']
        ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "success"}), 200


# ===============================
# API: Ambil data terbaru (Realtime)
# ===============================
@app.route('/api/latest')
def latest_data():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ax, ay, az, gx, gy, gz, created_at
        FROM accelerometer_data
        ORDER BY created_at DESC
        LIMIT 10
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(data)


if __name__ == "__main__":
    time.sleep(10)  # tunggu MySQL siap
    app.run(host="0.0.0.0", port=5000)
