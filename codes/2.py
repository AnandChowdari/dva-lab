# Experiment 2: Star Schema OLAP Operations (PostgreSQL)

sql_queries = """
-- Dimension Tables
CREATE TABLE dim_item (item_id INT PRIMARY KEY, item_name VARCHAR(50), category VARCHAR(50));
CREATE TABLE dim_location (location_id INT PRIMARY KEY, store_name VARCHAR(50), city VARCHAR(50));
CREATE TABLE dim_time (time_id INT PRIMARY KEY, date DATE, month INT, year INT);

-- Fact Table
CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    item_id INT REFERENCES dim_item(item_id),
    location_id INT REFERENCES dim_location(location_id),
    time_id INT REFERENCES dim_time(time_id),
    sales_amount DECIMAL(10, 2)
);

-- Materialized View
CREATE MATERIALIZED VIEW star_sales_cube AS
SELECT i.item_name, l.city, t.year, SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_item i ON f.item_id = i.item_id
JOIN dim_location l ON f.location_id = l.location_id
JOIN dim_time t ON f.time_id = t.time_id
GROUP BY CUBE (i.item_name, l.city, t.year);

-- Roll Up
SELECT item_name, SUM(total_sales) FROM star_sales_cube WHERE city IS NULL AND year IS NULL GROUP BY item_name;

-- Drill Down
SELECT item_name, city, total_sales FROM star_sales_cube WHERE item_name IS NOT NULL AND city IS NOT NULL;
"""

print(sql_queries)
