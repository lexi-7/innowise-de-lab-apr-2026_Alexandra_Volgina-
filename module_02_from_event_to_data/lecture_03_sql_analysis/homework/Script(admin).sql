--Задание 1: Работа с DML

INSERT INTO products (product_name, price, category_id, class, resistant, is_allergic, vitality_days)
VALUES 
    ('Ceremonial Matcha', 18.99, 15, 'C', 'No', 'Yes', 360),
    ('Red Caviar', 34.15, 6, 'A', 'No', 'Yes', 60);

SELECT * FROM products 
WHERE is_allergic = 'Yes' AND resistant = 'Yes';

UPDATE products 
SET is_allergic = 'Yes' 
WHERE product_name = 'Bananas Family Pack';

DELETE FROM products 
WHERE product_name = 'Red Caviar';

SELECT * FROM products ORDER BY product_id DESC LIMIT 10;

--Задание 2: Работа с DDL

CREATE TABLE Data_Layers (
    LayerID SERIAL PRIMARY KEY,
    LayerName VARCHAR(50) UNIQUE NOT NULL,
    Description TEXT
);

INSERT INTO Data_Layers (LayerName, Description) VALUES
    ('Bronze', 'Raw data layer - unprocessed data from sources'),
    ('Silver', 'Cleaned and validated data layer - transformed and quality checked'),
    ('Gold', 'Aggregated business layer - ready for analytics and reporting');

ALTER TABLE Data_Layers ADD COLUMN manager_email VARCHAR(100);

UPDATE Data_Layers SET manager_email = 
    CASE LayerName
        WHEN 'Bronze' THEN 'bronze.manager@ecmarket.com'
        WHEN 'Silver' THEN 'silver.manager@ecmarket.com'
        WHEN 'Gold' THEN 'gold.manager@ecmarket.com'
    END;

ALTER TABLE Data_Layers ADD CONSTRAINT unique_manager_email UNIQUE (manager_email);

ALTER TABLE shops RENAME COLUMN address TO shop_address;

--Задание 3: DCL (Управление доступом к данным)

CREATE ROLE data_engineer_trainee WITH LOGIN PASSWORD '123';

GRANT SELECT ON sales TO data_engineer_trainee;

GRANT INSERT, UPDATE ON sales TO data_engineer_trainee;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO data_engineer_trainee;

--Задание 4: DML/DCL (Сложные операции с пайплайнами)

UPDATE products 
SET price = price * 1.10 
WHERE category_id = (SELECT category_id FROM categories WHERE category_name = 'Fruits');

DELETE FROM employees 
WHERE employee_id NOT IN (SELECT DISTINCT employee_id FROM sales WHERE employee_id IS NOT NULL);

BEGIN;

INSERT INTO employees (first_name, last_name, birth_date, gender, city_id, shop_id, hire_date)
VALUES ('Anna', 'Volkova', '2000-05-12', 'F', 1, 1, CURRENT_DATE);

INSERT INTO sales (employee_id, customer_id, product_id, quantity, discount, total_price, sales_timestamp, transaction_number)
VALUES (LASTVAL(), 1, 1, 2, 0, 37.98, NOW(), 'TRX_' || TO_CHAR(NOW(), 'YYYYMMDDHH24MISS'));

COMMIT;

--Задание 5: Функции и Представления (Views для Gold Layer)

CREATE OR REPLACE FUNCTION AvgSalesPerEmployee(p_employee_id INTEGER)
RETURNS NUMERIC(10,2) AS $$
DECLARE
    avg_amount NUMERIC(10,2);
BEGIN
    SELECT AVG(total_price) INTO avg_amount
    FROM sales
    WHERE employee_id = p_employee_id;
    
    RETURN COALESCE(avg_amount, 0);
END;
$$ LANGUAGE plpgsql;

SELECT AvgSalesPerEmployee(5) AS average_sale_amount;

CREATE OR REPLACE VIEW FullStatShops AS
SELECT 
    sh.shop_id,
    sh.shop_address,
    co.country_name AS country,
    COUNT(s.sales_id) AS total_sales_count,
    COALESCE(SUM(s.total_price), 0) AS total_sales_amount
FROM shops sh
JOIN cities c ON sh.city_id = c.city_id
JOIN countries co ON c.country_id = co.country_id
LEFT JOIN employees e ON sh.shop_id = e.shop_id
LEFT JOIN sales s ON e.employee_id = s.employee_id
GROUP BY sh.shop_id, sh.shop_address, co.country_name;

SELECT * FROM FullStatShops ORDER BY total_sales_amount DESC LIMIT 10;

SELECT COUNT(*) FROM FullStatShops;

--Задание 6: DML (Управление платформой)

SELECT 
    e.employee_id,
    e.first_name,
    e.last_name,
    SUM(s.total_price) AS total_sales_amount
FROM employees e
JOIN sales s ON e.employee_id = s.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name
HAVING SUM(s.total_price) > 1000
ORDER BY total_sales_amount DESC;

UPDATE products 
SET class = 'A'
WHERE category_id IN (
    SELECT p.category_id
    FROM products p
    JOIN sales s ON p.product_id = s.product_id
    GROUP BY p.category_id
    HAVING SUM(s.total_price) > 5000
);

UPDATE products 
SET modify_timestamp = CURRENT_TIMESTAMP
WHERE modify_timestamp IS NULL;



