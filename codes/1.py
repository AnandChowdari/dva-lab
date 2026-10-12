# ==============================================================================
# LAB CYCLE - 1
# Aim: Perform OLAP operations using Materialized views and write SQL queries using Joins & Subqueries.
# ==============================================================================

sql_queries = """-- =============================================================================
-- PART 1: OLAP OPERATIONS USING MATERIALIZED VIEWS
-- =============================================================================

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
('Phone',  'Store1', '2024-06-01', 500.00),
('Laptop', 'Store2', '2024-06-01', 1500.00),
('Tablet', 'Store1', '2024-06-02', 750.00),
('Phone',  'Store2', '2024-06-02', 300.00),
('Laptop', 'Store3', '2024-07-01', 2000.00),
('Phone',  'Store3', '2024-07-01', 700.00),
('Tablet', 'Store2', '2024-07-02', 800.00),
('Laptop', 'Store1', '2024-07-02', 1700.00),
('Phone',  'Store1', '2024-07-02', 600.00);

-- 3. Create Materialized View (OLAP Cube)
CREATE MATERIALIZED VIEW sales_cube AS
SELECT item, location, time, SUM(sales_amount) AS total_sales
FROM sales
GROUP BY CUBE (item, location, time);

-- 4. Roll Up: Total sales of each item
SELECT item, total_sales
FROM sales_cube
WHERE item IS NOT NULL AND location IS NULL AND time IS NULL
ORDER BY item;

-- 5. Slice: Sales on 2024-06-01
SELECT item, location, total_sales
FROM sales_cube
WHERE time = '2024-06-01' AND item IS NOT NULL AND location IS NOT NULL
ORDER BY item, location;

-- 6. Dice: Laptop and Phone sold in Store1 and Store2 on 2024-06-01
SELECT item, location, total_sales
FROM sales_cube
WHERE item IN ('Laptop', 'Phone') AND location IN ('Store1', 'Store2')
  AND time = '2024-06-01'
ORDER BY item, location;

-- 7. Pivot: Item and location against June and July sales
SELECT item, location,
       SUM(CASE WHEN time BETWEEN '2024-06-01' AND '2024-06-30' THEN total_sales ELSE 0 END) AS sales_june,
       SUM(CASE WHEN time BETWEEN '2024-07-01' AND '2024-07-31' THEN total_sales ELSE 0 END) AS sales_july
FROM sales_cube
WHERE item IS NOT NULL AND location IS NOT NULL AND time IS NOT NULL
GROUP BY item, location
ORDER BY item, location;

-- 8. Drill Down: Item-wise sales broken down by location
SELECT item, location, total_sales
FROM sales_cube
WHERE item IS NOT NULL AND location IS NOT NULL AND time IS NULL
ORDER BY item, location;


-- =============================================================================
-- PART 2: SQL QUERIES USING JOINS & SUBQUERIES
-- =============================================================================

-- 1. Create Tables
CREATE TABLE department (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50)
);

CREATE TABLE employee (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    salary DECIMAL(10, 2),
    dept_id INT REFERENCES department(dept_id)
);

-- 2. Insert Data
INSERT INTO department VALUES
(1, 'Sales'), (2, 'HR'), (3, 'IT'), (4, 'Finance');

INSERT INTO employee VALUES
(101, 'Ravi',   50000, 1),
(102, 'Sita',   60000, 3),
(103, 'Kiran',  45000, 2),
(104, 'Anu',    70000, 3),
(105, 'Mohan',  40000, 1),
(106, 'Latha',  55000, NULL);

-- 3. Inner Join: Employees with their department
SELECT e.emp_name, d.dept_name
FROM employee e
INNER JOIN department d ON e.dept_id = d.dept_id
ORDER BY e.emp_id;

-- 4. Left Join: All employees, with department if available
SELECT e.emp_name, d.dept_name
FROM employee e
LEFT JOIN department d ON e.dept_id = d.dept_id
ORDER BY e.emp_id;

-- 5. Right Join: All departments, with employees if available
SELECT e.emp_name, d.dept_name
FROM employee e
RIGHT JOIN department d ON e.dept_id = d.dept_id
ORDER BY d.dept_id, e.emp_id;

-- 6. Full Join: All employees and all departments
SELECT e.emp_name, d.dept_name
FROM employee e
FULL JOIN department d ON e.dept_id = d.dept_id
ORDER BY d.dept_id, e.emp_id;

-- 7. Subquery: Employees earning more than the average salary
SELECT emp_name, salary
FROM employee
WHERE salary > (SELECT AVG(salary) FROM employee)
ORDER BY emp_id;

-- 8. Subquery with IN: Employees working in the IT department
SELECT emp_name, salary
FROM employee
WHERE dept_id IN (SELECT dept_id FROM department WHERE dept_name = 'IT')
ORDER BY emp_id;

-- 9. Subquery with NOT EXISTS: Departments having no employees
SELECT dept_name
FROM department d
WHERE NOT EXISTS (SELECT 1 FROM employee e WHERE e.dept_id = d.dept_id);

-- 10. Correlated Subquery: Employees earning more than their department average
SELECT e.emp_name, e.salary, e.dept_id
FROM employee e
WHERE e.salary > (SELECT AVG(salary) FROM employee WHERE dept_id = e.dept_id)
ORDER BY e.emp_id;"""

if __name__ == '__main__':
    print(sql_queries)
