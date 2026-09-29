import os
import mysql.connector
import subprocess
from dotenv import load_dotenv

load_dotenv()

def internet_ok():
    return subprocess.call(
        ["ping", "-c", "1", "8.8.8.8"],
        stdout=subprocess.DEVNULL
    ) == 0

if not internet_ok():
    exit()

local_db = mysql.connector.connect(
    host=os.environ["LOCAL_DB_HOST"],
    user=os.environ["LOCAL_DB_USER"],
    password=os.environ["LOCAL_DB_PASSWORD"],
    database=os.environ["LOCAL_DB_NAME"]
)

cloud_db = mysql.connector.connect(
    host=os.environ["CLOUD_DB_HOST"],
    user=os.environ["CLOUD_DB_USER"],
    password=os.environ["CLOUD_DB_PASSWORD"],
    database=os.environ["CLOUD_DB_NAME"]
)

lcur = local_db.cursor(dictionary=True)
ccur = cloud_db.cursor()

lcur.execute("SELECT * FROM accelerometer_data WHERE synced = 0")
rows = lcur.fetchall()

for r in rows:
    ccur.execute("""
        INSERT INTO sensor_data_backup
        (ax, ay, az, gx, gy, gz, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        r['ax'], r['ay'], r['az'],
        r['gx'], r['gy'], r['gz'],
        r['created_at']
    ))

lcur.execute("UPDATE accelerometer_data SET synced = 1 WHERE synced = 0")

cloud_db.commit()
local_db.commit()