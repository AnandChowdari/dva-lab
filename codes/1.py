# Experiment 1: OLAP Operations Using Materialized Views (PostgreSQL)

sql_queries = """
-- 1. Create Base Sales Table
CREATE TABLE sales (
    item VARCHAR(50),
    location VARCHAR(50),
    time DATE,
    sales_amount DECIMAL(10, 2)
);

-- 2. Insert Sample Data
INSERT INTO sales (item, location, time, sales_amount) VALUES
    ('Laptop', 'Store1', '2024-06-01', 1000.00),
    ('Phone',  'Store1', '2024-06-01',  500.00),
    ('Laptop', 'Store2', '2024-06-01', 1500.00),
    ('Tablet', 'Store1', '2024-06-02',  750.00),
    ('Phone',  'Store2', '2024-06-02',  300.00),
    ('Laptop', 'Store3', '2024-07-01', 2000.00),
    ('Phone',  'Store3', '2024-07-01',  700.00),
    ('Tablet', 'Store2', '2024-07-02',  800.00),
    ('Laptop', 'Store1', '2024-07-02', 1700.00),
    ('Phone',  'Store1', '2024-07-02',  600.00);

-- 3. Create Materialized View (OLAP Cube)
CREATE MATERIALIZED VIEW sales_cube AS
SELECT item, location, time, SUM(sales_amount) AS total_sales
FROM sales
GROUP BY CUBE (item, location, time);

-- 4. Roll Up (Sales by item)
SELECT item, SUM(total_sales) AS total_sales
FROM sales_cube
WHERE location IS NULL AND time IS NULL AND item IS NOT NULL
GROUP BY item;

-- 5. Slice (time = '2024-06-01')
SELECT item, location, total_sales
FROM sales_cube
WHERE time = '2024-06-01' AND item IS NOT NULL AND location IS NOT NULL;

-- 6. Dice (Laptop & Phone in Store1 & Store2 on '2024-06-01')
SELECT item, location, total_sales
FROM sales_cube
WHERE item IN ('Laptop', 'Phone')
  AND location IN ('Store1', 'Store2')
  AND time = '2024-06-01';

-- 7. Pivot (June vs July cross-tab)
SELECT 
    item, 
    location,
    SUM(CASE WHEN time = '2024-06-01' THEN total_sales ELSE 0 END) AS sales_june,
    SUM(CASE WHEN time = '2024-07-01' THEN total_sales ELSE 0 END) AS sales_july
FROM sales_cube
GROUP BY item, location;
"""

print(sql_queries)
