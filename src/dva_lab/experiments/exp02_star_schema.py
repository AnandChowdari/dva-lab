"""Experiment 2: Star Schema OLAP Operations using Materialized Views."""

from typing import Any, Optional
from .base import Experiment

NUMBER = 2
TITLE = "Star Schema OLAP Operations Using Materialized Views"
CATEGORY = "OLAP & Data Warehousing (SQL)"
AIM = "Perform OLAP operations by creating and using Materialized views based on a Star schema."
DEPENDENCIES = ["PostgreSQL 12+"]

CONCEPT = """\
A Star Schema organizes data into central fact tables containing numerical metrics and \
surrounding dimension tables with descriptive attributes. Materialized views allow \
pre-aggregating across multiple joined dimensions (CUBE).\
"""

CODE = """\
-- 1. Create Dimension Tables
CREATE TABLE dim_time (
    time_id INT PRIMARY KEY,
    day DATE,
    month VARCHAR(20),
    quarter VARCHAR(5),
    year INT
);

INSERT INTO dim_time VALUES
(1, '2024-06-01', 'June', 'Q2', 2024),
(2, '2024-06-02', 'June', 'Q2', 2024),
(3, '2024-06-15', 'June', 'Q2', 2024),
(4, '2024-07-01', 'July', 'Q3', 2024),
(5, '2024-07-02', 'July', 'Q3', 2024),
(6, '2024-07-03', 'July', 'Q3', 2024),
(7, '2024-08-01', 'August', 'Q3', 2024),
(8, '2024-08-15', 'August', 'Q3', 2024);

CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    item_name VARCHAR(50),
    brand VARCHAR(50),
    category VARCHAR(50)
);

INSERT INTO dim_product VALUES
(1, 'Laptop',     'BrandA', 'Electronics'),
(2, 'Phone',      'BrandB', 'Electronics'),
(3, 'Tablet',     'BrandA', 'Electronics'),
(4, 'Headphones', 'BrandC', 'Accessories'),
(5, 'Smartwatch', 'BrandB', 'Accessories'),
(6, 'Monitor',    'BrandA', 'Electronics'),
(7, 'Keyboard',   'BrandD', 'Accessories'),
(8, 'Charger',    'BrandE', 'Accessories');

CREATE TABLE dim_city (
    city_id INT PRIMARY KEY,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50)
);

INSERT INTO dim_city VALUES
(1, 'CityA', 'State1', 'Country1'),
(2, 'CityB', 'State1', 'Country1'),
(3, 'CityC', 'State2', 'Country1'),
(4, 'CityD', 'State2', 'Country1'),
(5, 'CityE', 'State3', 'Country1'),
(6, 'CityF', 'State3', 'Country1'),
(7, 'CityG', 'State4', 'Country1'),
(8, 'CityH', 'State4', 'Country1');

-- 2. Create Fact Table
CREATE TABLE fact_sales (
    sales_id INT PRIMARY KEY,
    product_id INT REFERENCES dim_product(product_id),
    city_id INT REFERENCES dim_city(city_id),
    time_id INT REFERENCES dim_time(time_id),
    sales_amount DECIMAL(10, 2)
);

INSERT INTO fact_sales VALUES
(1, 1, 1, 1, 1000.00),
(2, 2, 1, 1,  500.00),
(3, 1, 2, 2, 1500.00),
(4, 3, 1, 3,  750.00),
(5, 2, 2, 4,  300.00),
(6, 1, 3, 5, 2000.00),
(7, 3, 4, 6,  800.00),
(8, 5, 5, 7,  600.00);

-- 3. Create Materialized View
CREATE MATERIALIZED VIEW sales_cube AS
SELECT p.category, p.item_name, c.state, c.city, t.month,
       SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
JOIN dim_city c    ON f.city_id    = c.city_id
JOIN dim_time t    ON f.time_id    = t.time_id
GROUP BY CUBE (p.category, p.item_name, c.state, c.city, t.month);

-- 4. Roll Up: Total sales by product category
SELECT category, total_sales FROM sales_cube
WHERE category IS NOT NULL AND item_name IS NULL AND state IS NULL
  AND city IS NULL AND month IS NULL
ORDER BY category;

-- 5. Drill Down: Sales of Electronics by city
SELECT city, total_sales FROM sales_cube
WHERE category = 'Electronics' AND item_name IS NULL AND state IS NULL
  AND city IS NOT NULL AND month IS NULL
ORDER BY city;

-- 6. Slice: Sales in June
SELECT item_name, city, total_sales FROM sales_cube
WHERE month = 'June' AND item_name IS NOT NULL AND city IS NOT NULL
  AND category IS NULL AND state IS NULL
ORDER BY item_name, city;

-- 7. Dice: Laptop and Phone in CityA and CityB for June
SELECT item_name, city, total_sales FROM sales_cube
WHERE item_name IN ('Laptop','Phone') AND city IN ('CityA','CityB')
  AND month = 'June' AND category IS NULL AND state IS NULL
ORDER BY item_name, city;

-- 8. Pivot: Sales by item and month
SELECT item_name,
       SUM(CASE WHEN month = 'June'   THEN total_sales ELSE 0 END) AS june,
       SUM(CASE WHEN month = 'July'   THEN total_sales ELSE 0 END) AS july,
       SUM(CASE WHEN month = 'August' THEN total_sales ELSE 0 END) AS august
FROM sales_cube
WHERE item_name IS NOT NULL AND month IS NOT NULL AND category IS NULL
  AND state IS NULL AND city IS NULL
GROUP BY item_name
ORDER BY item_name;\
"""

OUTPUT = """\
Star schema queries executed successfully.
"""


class Exp02StarSchema(Experiment):
    number = NUMBER
    title = TITLE
    category = CATEGORY
    aim = AIM
    concept = CONCEPT
    code = CODE
    output = OUTPUT
    dependencies = DEPENDENCIES
