DROP DATABASE IF EXISTS tourism_portal;

CREATE DATABASE tourism_portal;

USE tourism_portal;


CREATE TABLE users (

id INT AUTO_INCREMENT PRIMARY KEY,

name VARCHAR(100),

email VARCHAR(120) UNIQUE,

password VARCHAR(255),

role ENUM('admin','user') DEFAULT 'user'

);

INSERT INTO users(name,email,password,role)
VALUES ('Admin','admin@tourism.com','admin123','admin');



CREATE TABLE states (

id INT AUTO_INCREMENT PRIMARY KEY,

state_name VARCHAR(120),

description TEXT,

image VARCHAR(255)

);

INSERT INTO states(state_name,description,image) VALUES

('Uttar Pradesh','Spiritual tourism including Varanasi and Taj Mahal','uttarpradesh.jpg'),

('Tamil Nadu','Famous for temples and heritage','tamilnadu.jpg'),

('Karnataka','Hampi ruins and Coorg hills','karnataka.jpg'),

('Rajasthan','Land of forts and palaces','rajasthan.jpg'),

('Gujarat','Rann of Kutch and Gir forest','gujarat.jpg');



CREATE TABLE places (

id INT AUTO_INCREMENT PRIMARY KEY,

place_name VARCHAR(150),

state_id INT,

description TEXT,

image VARCHAR(255),

FOREIGN KEY(state_id) REFERENCES states(id)

);

INSERT INTO places(place_name,state_id,description,image) VALUES

('Taj Mahal',1,'World famous monument in Agra','tajmahal.jpg'),

('Varanasi Ghats',1,'Sacred ghats of river Ganges','varanasi.jpg'),

('Meenakshi Temple',2,'Historic temple in Madurai','meenakshi.jpg'),

('Ooty Hill Station',2,'Beautiful hill station','ooty.jpg'),

('Hampi Ruins',3,'Ancient Vijayanagara ruins','hampi.jpg'),

('Rajasthan Forts',4,'Majestic forts across Rajasthan','rajasthanforts.jpg'),

('Rann of Kutch',5,'Salt desert with cultural festivals','kutch.jpg');



CREATE TABLE place_images (

id INT AUTO_INCREMENT PRIMARY KEY,

place_id INT,

image VARCHAR(255),

FOREIGN KEY(place_id) REFERENCES places(id)

);

INSERT INTO place_images(place_id,image) VALUES

(1,'taj1.jpg'),
(1,'taj2.jpg'),

(2,'varanasi1.jpg'),
(2,'varanasi2.jpg'),

(3,'meenakshi1.jpg'),
(3,'meenakshi2.jpg'),

(4,'ooty1.jpg'),
(4,'ooty2.jpg'),

(5,'hampi1.jpg'),
(5,'hampi2.jpg'),

(6,'rajasthanforts1.jpg'),
(6,'rajasthanforts2.jpg'),

(7,'kutch1.jpg'),
(7,'kutch2.jpg');



CREATE TABLE contact_messages (

id INT AUTO_INCREMENT PRIMARY KEY,

name VARCHAR(100),

email VARCHAR(120),

message TEXT

);