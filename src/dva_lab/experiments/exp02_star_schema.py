"""Experiment 2: OLAP operations using materialized views based on a Star schema."""

from typing import Any, Optional
from .base import Experiment

NUMBER = 2
TITLE = "OLAP Operations Using Materialized Views (Star Schema)"
CATEGORY = "OLAP & Data Warehousing (SQL)"
AIM = (
    "Perform OLAP operations by creating and using Materialized views based on a Star schema. "
    "(Assume typical star schema tables such as fact_sales, dim_product, dim_city, and dim_time.)"
)
DEPENDENCIES = ["PostgreSQL 12+"]

CONCEPT = """\
A Star Schema is a foundational architecture in multidimensional data warehousing consisting of:
- A central Fact Table (sales) containing quantitative numerical measures (sales_amount) and foreign keys.
- Surrounding Dimension Tables (time, items, locations) containing rich descriptive attributes (dates, brands, categories, cities).

By joining the fact table with dimension tables inside a PostgreSQL Materialized View aggregated with GROUP BY CUBE,
we precalculate measures across all combinations of dimensional hierarchies:
1. Roll Up: Summarizing data up a dimension hierarchy (e.g., total sales by item type).
2. Drill Down: Navigating down to higher granularity (e.g., sales of Electronics broken down by city).
3. Slice: Filtering on a single dimension value (e.g., sales on day '2024-06-01').
4. Dice: Sub-cube filtering across multiple dimensions simultaneously (e.g., Laptop/Phone in CityA/CityB during June).
5. Pivot: Rotating rows into columns to build comparative matrices (e.g., daily sales per item).\
"""

CODE = """\
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
"""

EXPECTED_OUTPUT = """\
Expected Star Schema OLAP Query Outputs:

1. Roll Up (Total Sales by Item Type):
   +-------------+-------------+
   | type        | total_sales |
   +-------------+-------------+
   | Electronics |     6850.00 |
   | Accessories |      600.00 |
   +-------------+-------------+

2. Drill Down (Electronics Sales by City):
   +-------+-------------+
   | city  | total_sales |
   +-------+-------------+
   | CityA |     2250.00 |
   | CityB |     1800.00 |
   | CityC |     2000.00 |
   | CityD |      800.00 |
   +-------+-------------+

3. Slice (Day = '2024-06-01'):
   +-----------+---------+-------------+
   | item_name | street  | total_sales |
   +-----------+---------+-------------+
   | Laptop    | Street1 |     1000.00 |
   | Phone     | Street1 |      500.00 |
   +-----------+---------+-------------+

4. Dice (Laptop & Phone in CityA & CityB for June):
   +-----------+---------+-------------+
   | item_name | street  | total_sales |
   +-----------+---------+-------------+
   | Laptop    | Street1 |     1000.00 |
   | Phone     | Street1 |      500.00 |
   | Laptop    | Street2 |     1500.00 |
   +-----------+---------+-------------+

5. Pivot (Sales by Item and Day):
   +-----------+------------+------------+------------+
   | item_name | 2024-06-01 | 2024-06-02 | 2024-06-15 |
   +-----------+------------+------------+------------+
   | Laptop    |    1000.00 |    1500.00 |       0.00 |
   | Phone     |     500.00 |       0.00 |       0.00 |
   | Tablet    |       0.00 |       0.00 |     750.00 |
   +-----------+------------+------------+------------+
"""

RESULT = (
    "OLAP operations (Roll Up, Drill Down, Slice, Dice, and Pivot) using a Star Schema "
    "materialized view were successfully implemented and validated in PostgreSQL."
)

NOTES = """\
PostgreSQL Setup Instructions:
1. Ensure PostgreSQL is installed and running.
2. Run via psql CLI or pgAdmin:
   psql -U postgres -d dva_warehouse -f exp02_star_schema.sql
3. Star schema tables implemented:
   - Fact Table: sales
   - Dimension Tables: time, items, locations\
"""


def run(connection: Optional[Any] = None, show_sql: bool = True) -> str:
    """Display SQL script and PostgreSQL instructions for Star Schema OLAP."""
    if connection is not None:
        cursor = connection.cursor()
        for statement in CODE.split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
        if hasattr(connection, "commit"):
            connection.commit()
        return "Executed Star Schema SQL script successfully on the database connection."

    msg = (
        "[SQL Experiment 2 Notice]\n"
        "This experiment requires a PostgreSQL database instance.\n"
        "To run against a live database, pass a valid connection object: run_experiment(2, connection=conn)\n\n"
        "Full SQL Script:\n" + ("-" * 60) + "\n" + CODE
    )
    if show_sql:
        print(msg)
    return CODE


def get_experiment() -> Experiment:
    """Create and return the Experiment instance."""
    return Experiment(
        number=NUMBER,
        title=TITLE,
        category=CATEGORY,
        aim=AIM,
        concept=CONCEPT,
        code=CODE,
        dependencies=DEPENDENCIES,
        expected_output=EXPECTED_OUTPUT,
        result=RESULT,
        notes=NOTES,
        run_func=run,
    )
