CREATE DATABASE IF NOT EXISTS user_data;

USE user_data;

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(64) PRIMARY KEY,
    email VARCHAR(64) NOT NULL,
    body VARCHAR(1000)
);