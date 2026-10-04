CREATE DATABASE IF NOT EXISTS agriproject_db;

USE agriproject_db;

---                                 Tables

CREATE TABLE IF NOT EXISTS cities (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL UNIQUE,
    province VARCHAR(100),
    region VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS markets (
    market_id INT AUTO_INCREMENT PRIMARY KEY,
    market_name VARCHAR(150) NOT NULL,
    city_id INT NOT NULL,
    FOREIGN KEY (city_id)
        REFERENCES cities(city_id)
);


CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS subcategories (
    subcategory_id INT AUTO_INCREMENT PRIMARY KEY,
    subcategory_name VARCHAR(100) NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);


CREATE TABLE IF NOT EXISTS units (
    unit_id INT AUTO_INCREMENT PRIMARY KEY,
    unit_name VARCHAR(30) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category_id INT NOT NULL,
    unit_id INT,
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id),
    FOREIGN KEY (unit_id)
        REFERENCES units(unit_id)
);


CREATE TABLE IF NOT EXISTS sources (
    source_id INT AUTO_INCREMENT PRIMARY KEY,
    source_type VARCHAR(20) NOT NULL,
    source_name VARCHAR(200) NOT NULL,
    source_url TEXT
);


CREATE TABLE IF NOT EXISTS price_records (
    price_id INT AUTO_INCREMENT PRIMARY KEY,
    price_date DATE NOT NULL,
    market_id INT NOT NULL,
    item_id INT NOT NULL,
    source_id INT NOT NULL,
    price_min DECIMAL(10,2),
    price_max DECIMAL(10,2),
    price_average DECIMAL(10,2),
    currency VARCHAR(10) DEFAULT 'PHP',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    specification VARCHAR(200),
    FOREIGN KEY (market_id) REFERENCES markets(market_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (source_id) REFERENCES sources(source_id)
);


ALTER TABLE price_records
ADD CONSTRAINT unique_daily_price
UNIQUE (
    price_date,
    market_id,
    item_id,
    source_id
);


---                             Duplicate protection:

ALTER TABLE price_records
ADD CONSTRAINT unique_daily_price
UNIQUE (
    price_date,
    market_id,
    item_id,
    source_id
);

---                             Fixed reference data

---Cities
INSERT INTO cities
(city_name, province, region)
VALUES
('Paranaque', 'Metro Manila', 'NCR'),
('Las Pinas', 'Metro Manila', 'NCR'),
('Muntinlupa', 'Metro Manila', 'NCR');


