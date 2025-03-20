DROP DATABASE IF EXISTS boat_reservation_db;
CREATE DATABASE boat_reservation_db;
USE boat_reservation_db;

CREATE TABLE sailors (
    sailor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE boats (
    boat_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    capacity INT NOT NULL
);

CREATE TABLE reserves (
    reserve_id INT AUTO_INCREMENT PRIMARY KEY,
    sailor_id INT,
    boat_id INT,
    reserve_date DATE,
    FOREIGN KEY (sailor_id) REFERENCES sailors(sailor_id) ON DELETE CASCADE,
    FOREIGN KEY (boat_id) REFERENCES boats(boat_id) ON DELETE CASCADE
);


INSERT INTO sailors (name, password) VALUES ('John Doe', 'password123');
INSERT INTO boats (name, capacity) VALUES ('Sea Explorer', 4);

select * from sailors;
