"""Experiment 1: OLAP operations using materialized views."""

from typing import Any, Optional
from .base import Experiment

NUMBER = 1
TITLE = "OLAP Operations Using Materialized Views"
CATEGORY = "OLAP & Data Warehousing (SQL)"
AIM = "Perform OLAP operations using Materialized views."
DEPENDENCIES = ["PostgreSQL 12+"]

CONCEPT = """\
On-Line Analytical Processing (OLAP) enables rapid, multidimensional data analysis for \
decision-making. In PostgreSQL, a Materialized View physically caches the precomputed \
result of a query (including GROUP BY CUBE aggregations) on disk, drastically reducing query \
latency compared to re-aggregating millions of rows from transactional tables.

Key OLAP Operations Demonstrated:
1. Roll Up: Aggregation by climbing up a hierarchy (e.g., total sales grouped by item, collapsing location and time).
2. Slice: Selecting a single rectangular slice from the data cube by fixing one dimension (e.g., date = '2024-06-01').
3. Dice: Defining a sub-cube by applying condition filters on two or more dimensions simultaneously.
4. Pivot (Rotate): Transforming row values into columns (cross-tabulation) using conditional aggregation (CASE WHEN).\
"""

CODE = """\
-- ============================================================================
-- Experiment 1: OLAP Operations Using Materialized Views
-- Database: PostgreSQL 12+
-- Note: Fixed line-break typo in original record: '2024-0601' -> '2024-06-01'
-- ============================================================================

-- 1. Create Base Sales Table
DROP TABLE IF EXISTS sales CASCADE;
CREATE TABLE sales (
    item VARCHAR(50),
    location VARCHAR(50),
    time DATE,
    sales_amount DECIMAL(10, 2)
);

-- 2. Insert Sample Transaction Data
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

-- 3. Create Materialized View Representing the OLAP Data Cube
DROP MATERIALIZED VIEW IF EXISTS sales_cube;
CREATE MATERIALIZED VIEW sales_cube AS
SELECT 
    item, 
    location, 
    time, 
    SUM(sales_amount) AS total_sales
FROM sales
GROUP BY CUBE(item, location, time);

-- 4. OLAP Operation: Roll Up (Total Sales by Item across all locations and dates)
SELECT item, SUM(total_sales) AS total_sales
FROM sales_cube
WHERE location IS NULL AND time IS NULL
GROUP BY item;

-- 5. OLAP Operation: Slice (Sales for a specific date: '2024-06-01')
SELECT item, location, total_sales
FROM sales_cube
WHERE time = '2024-06-01';

-- 6. OLAP Operation: Dice (Laptops and Phones in Store1 and Store2 on '2024-06-01')
SELECT item, location, total_sales
FROM sales_cube
WHERE item IN ('Laptop', 'Phone') 
  AND location IN ('Store1', 'Store2') 
  AND time = '2024-06-01';

-- 7. OLAP Operation: Pivot (Cross-tabulation comparing June vs July Sales)
SELECT 
    item, 
    location,
    SUM(CASE WHEN time = '2024-06-01' THEN total_sales ELSE 0 END) AS sales_june,
    SUM(CASE WHEN time = '2024-07-01' THEN total_sales ELSE 0 END) AS sales_july
FROM sales_cube
GROUP BY item, location;
"""

EXPECTED_OUTPUT = """\
Expected SQL Query Results:

1. Roll Up (Sales by Item):
   +--------+-------------+
   | item   | total_sales |
   +--------+-------------+
   | Laptop |     6200.00 |
   | Phone  |     2100.00 |
   | Tablet |     1550.00 |
   +--------+-------------+

2. Slice (time = '2024-06-01'):
   +--------+----------+-------------+
   | item   | location | total_sales |
   +--------+----------+-------------+
   | Laptop | Store1   |     1000.00 |
   | Phone  | Store1   |      500.00 |
   | Laptop | Store2   |     1500.00 |
   +--------+----------+-------------+

3. Dice (items IN ('Laptop', 'Phone') AND location IN ('Store1', 'Store2') AND time = '2024-06-01'):
   +--------+----------+-------------+
   | item   | location | total_sales |
   +--------+----------+-------------+
   | Laptop | Store1   |     1000.00 |
   | Phone  | Store1   |      500.00 |
   | Laptop | Store2   |     1500.00 |
   +--------+----------+-------------+

4. Pivot (Cross-tabulation June 1 vs July 1):
   +--------+----------+------------+------------+
   | item   | location | sales_june | sales_july |
   +--------+----------+------------+------------+
   | Laptop | Store1   |    1000.00 |       0.00 |
   | Laptop | Store2   |    1500.00 |       0.00 |
   | Laptop | Store3   |       0.00 |    2000.00 |
   | Phone  | Store1   |     500.00 |       0.00 |
   | Phone  | Store3   |       0.00 |     700.00 |
   +--------+----------+------------+------------+
"""

RESULT = "OLAP operations (Roll Up, Slice, Dice, and Pivot) using materialized views were successfully formulated and executed."

NOTES = """\
Execution Instructions for PostgreSQL:
1. Ensure PostgreSQL is installed and a database is accessible (e.g., via psql or pgAdmin).
2. Connect to your database: `psql -U postgres -d your_db`
3. Execute the SQL script: `\\i exp01_olap.sql` or copy-paste the query blocks into your SQL editor.
4. Record Correction: The original PDF contained a typographical split in the Dice query date ('2024-\\n0601'). This has been standardized to '2024-06-01'.\
"""


def run(connection: Optional[Any] = None, show_sql: bool = True) -> str:
    """Display SQL script and PostgreSQL instructions.

    To execute against an active PostgreSQL database, pass a DBAPI or SQLAlchemy
    connection object.
    """
    if connection is not None:
        cursor = connection.cursor()
        for statement in CODE.split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
        if hasattr(connection, "commit"):
            connection.commit()
        return "Executed SQL script successfully on the provided database connection."

    msg = (
        "[SQL Experiment 1 Notice]\n"
        "This experiment requires a PostgreSQL database instance.\n"
        "To run against a live database, pass a valid connection object: run_experiment(1, connection=conn)\n\n"
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
