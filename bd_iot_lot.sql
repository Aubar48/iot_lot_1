CREATE DATABASE iot_data;

USE iot_data;

CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor VARCHAR(50),
    value FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
