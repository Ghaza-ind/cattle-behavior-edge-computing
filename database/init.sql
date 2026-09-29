CREATE DATABASE cow_behavior;


USE cow_behavior;


CREATE TABLE accelerometer_data (
id INT AUTO_INCREMENT PRIMARY KEY,
ax FLOAT,
ay FLOAT,
az FLOAT,
gx FLOAT,
gy FLOAT,
gz FLOAT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);