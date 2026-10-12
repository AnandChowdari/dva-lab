-- ============================================================================
-- Experiment 2: OLAP Operations Based on Star Schema Using Materialized Views
-- Database: PostgreSQL 12+
-- Schema: Star Schema (Dimension: time, items, locations | Fact: sales)
-- ============================================================================

-- 1. Create Dimension Tables
DROP TABLE IF EXISTS sales CASCADE;
DROP TABLE IF EXISTS time CASCADE;
DROP TABLE IF EXISTS items CASCADE;
DROP TABLE IF EXISTS locations CASCADE;

CREATE TABLE time (
    time_id INT PRIMARY KEY,
    day DATE,
    month VARCHAR(50),
    quarter VARCHAR(50),
    year INT
);

CREATE TABLE items (
    item_id INT PRIMARY KEY,
    item_name VARCHAR(50),
    brand VARCHAR(50),
    type VARCHAR(50)
);

CREATE TABLE locations (
    location_id INT PRIMARY KEY,
    street VARCHAR(50),
    city VARCHAR(50),
    province_or_state VARCHAR(50),
    country VARCHAR(50)
);

-- 2. Create Central Fact Table
CREATE TABLE sales (
    sales_id INT PRIMARY KEY,
    item_id INT REFERENCES items(item_id),
    location_id INT REFERENCES locations(location_id),
    time_id INT REFERENCES time(time_id),
    sales_amount DECIMAL(10, 2)
);

-- 3. Populate Dimension Data
INSERT INTO time (time_id, day, month, quarter, year) VALUES
    (1, '2024-06-01', 'June', 'Q2', 2024),
    (2, '2024-06-02', 'June', 'Q2', 2024),
    (3, '2024-06-15', 'June', 'Q2', 2024),
    (4, '2024-07-01', 'July', 'Q3', 2024),
    (5, '2024-07-02', 'July', 'Q3', 2024),
    (6, '2024-07-03', 'July', 'Q3', 2024),
    (7, '2024-08-01', 'August', 'Q3', 2024),
    (8, '2024-08-15', 'August', 'Q3', 2024);

INSERT INTO items (item_id, item_name, brand, type) VALUES
    (1, 'Laptop',     'BrandA', 'Electronics'),
    (2, 'Phone',      'BrandB', 'Electronics'),
    (3, 'Tablet',     'BrandA', 'Electronics'),
    (4, 'Headphones', 'BrandC', 'Accessories'),
    (5, 'Smartwatch', 'BrandB', 'Accessories'),
    (6, 'Monitor',    'BrandA', 'Electronics'),
    (7, 'Keyboard',   'BrandD', 'Accessories'),
    (8, 'Charger',    'BrandE', 'Accessories');

INSERT INTO locations (location_id, street, city, province_or_state, country) VALUES
    (1, 'Street1', 'CityA', 'State1', 'Country1'),
    (2, 'Street2', 'CityB', 'State1', 'Country1'),
    (3, 'Street3', 'CityC', 'State2', 'Country1'),
    (4, 'Street4', 'CityD', 'State2', 'Country1'),
    (5, 'Street5', 'CityE', 'State3', 'Country1'),
    (6, 'Street6', 'CityF', 'State3', 'Country1'),
    (7, 'Street7', 'CityG', 'State4', 'Country1'),
    (8, 'Street8', 'CityH', 'State4', 'Country1');

-- 4. Populate Fact Table Data
INSERT INTO sales (sales_id, item_id, location_id, time_id, sales_amount) VALUES
    (1, 1, 1, 1, 1000.00),
    (2, 2, 1, 1,  500.00),
    (3, 1, 2, 2, 1500.00),
    (4, 3, 1, 3,  750.00),
    (5, 2, 2, 4,  300.00),
    (6, 1, 3, 5, 2000.00),
    (7, 3, 4, 6,  800.00),
    (8, 5, 5, 7,  600.00);

-- 5. Create Star Schema Materialized View (OLAP Data Cube)
DROP MATERIALIZED VIEW IF EXISTS sales_cube;
CREATE MATERIALIZED VIEW sales_cube AS
SELECT 
    t.day, t.month, t.quarter, t.year,
    i.item_name, i.brand, i.type,
    l.street, l.city, l.province_or_state, l.country,
    SUM(s.sales_amount) AS total_sales
FROM sales s
JOIN time t ON s.time_id = t.time_id
JOIN items i ON s.item_id = i.item_id
JOIN locations l ON s.location_id = l.location_id
GROUP BY CUBE(
    t.day, t.month, t.quarter, t.year,
    i.item_name, i.brand, i.type,
    l.street, l.city, l.province_or_state, l.country
);

-- 6. OLAP Operation 1: Roll Up (Total Sales by Item Type)
SELECT i.type, SUM(s.total_sales) AS total_sales
FROM sales_cube s
JOIN items i ON s.item_name = i.item_name
GROUP BY i.type;

-- 7. OLAP Operation 2: Drill Down (Sales of Electronics by City)
SELECT l.city, SUM(s.total_sales) AS total_sales
FROM sales_cube s
JOIN items i ON s.item_name = i.item_name
JOIN locations l ON s.street = l.street
WHERE i.type = 'Electronics'
GROUP BY l.city;

-- 8. OLAP Operation 3: Slice (Sales for Day '2024-06-01')
SELECT s.item_name, s.street, s.total_sales
FROM sales_cube s
WHERE s.day = '2024-06-01';

-- 9. OLAP Operation 4: Dice (Laptop and Phone in CityA and CityB for June)
SELECT s.item_name, s.street, s.total_sales
FROM sales_cube s
WHERE s.item_name IN ('Laptop', 'Phone')
  AND s.city IN ('CityA', 'CityB')
  AND s.month = 'June';

-- 10. OLAP Operation 5: Pivot (Daily sales per item across June dates)
SELECT s.item_name,
    SUM(CASE WHEN s.day = '2024-06-01' THEN s.total_sales ELSE 0 END) AS "2024-06-01",
    SUM(CASE WHEN s.day = '2024-06-02' THEN s.total_sales ELSE 0 END) AS "2024-06-02",
    SUM(CASE WHEN s.day = '2024-06-15' THEN s.total_sales ELSE 0 END) AS "2024-06-15"
FROM sales_cube s
GROUP BY s.item_name;
