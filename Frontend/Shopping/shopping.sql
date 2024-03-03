CREATE DATABASE IF NOT EXISTS item;

USE item;

CREATE TABLE IF NOT EXISTS item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL
);

INSERT INTO `item` (`id`, `name`, `price`, `quantity`) VALUES
('1', 'Travel Insurance Bronze', '82.00', '1'),
('2', 'Neck Pillow', '14.99', '1'),
('3', 'SQ One Way to Tokyo', '399.00', '1'),
('4', 'ANA One Way to Tokyo', '402.00', '1'),
('5', 'Ground Tour Seoul', '43.42', '1'),
('6', 'Great Wall of China Pass', '15.00', '1'),
('7', 'E-Sim Unlimited Wifi 10 Days', '23.00', '1'),
('8', 'Travel Wifi Router 7 Days', '30.00', '1');