CREATE DATABASE IF NOT EXISTS item;

USE item;

CREATE TABLE IF NOT EXISTS item (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL
);

INSERT INTO `item` (`id`, `name`, `price`, `quantity`) VALUES
('price_1OsRBkATlCeKbEIxRqhWm7kZ', 'Travel Insurance Bronze', '82.00', '1'),
('price_1OuAfoATlCeKbEIxhCUtH2hV', 'Neck Pillow', '14.99', '1'),
('price_1OuAg6ATlCeKbEIxywMYo4Ql', 'SQ One Way to Tokyo', '399.00', '1'),
('price_1OuAgKATlCeKbEIxKMzjAWzF', 'ANA One Way to Tokyo', '402.00', '1'),
('price_1OuAgeATlCeKbEIxG3yFhvUZ', 'Ground Tour Seoul', '43.42', '1'),
('price_1OuAgrATlCeKbEIxwEaLl9le', 'Great Wall of China Pass', '15.00', '1'),
('price_1OuAh8ATlCeKbEIxeXu2tGvh', 'E-Sim Unlimited Wifi 10 Days', '23.00', '1'),
('price_1OuAhOATlCeKbEIxatb7OYUQ', 'Travel Wifi Router 7 Days', '30.00', '1');