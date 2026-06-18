-- Enable transaction
BEGIN;

-- PK

ALTER TABLE silver.silver_countries 
ADD CONSTRAINT pk_silver_countries PRIMARY KEY (country_id);

ALTER TABLE silver.silver_cities 
ADD CONSTRAINT pk_silver_cities PRIMARY KEY (city_id);

ALTER TABLE silver.silver_categories 
ADD CONSTRAINT pk_silver_categories PRIMARY KEY (category_id);

ALTER TABLE silver.silver_products 
ADD CONSTRAINT pk_silver_products PRIMARY KEY (product_id);

ALTER TABLE silver.silver_shops 
ADD CONSTRAINT pk_silver_shops PRIMARY KEY (shop_id);

ALTER TABLE silver.silver_employees 
ADD CONSTRAINT pk_silver_employees PRIMARY KEY (employee_id);

ALTER TABLE silver.silver_customers 
ADD CONSTRAINT pk_silver_customers PRIMARY KEY (customer_id);

ALTER TABLE silver.silver_sales 
ADD CONSTRAINT pk_silver_sales PRIMARY KEY (sales_id);

-- FK

-- Cities -> Countries
ALTER TABLE silver.silver_cities 
ADD CONSTRAINT fk_silver_cities_country 
FOREIGN KEY (country_id) 
REFERENCES silver.silver_countries(country_id);

-- Products -> Categories
ALTER TABLE silver.silver_products 
ADD CONSTRAINT fk_silver_products_category 
FOREIGN KEY (category_id) 
REFERENCES silver.silver_categories(category_id);

-- Shops -> Cities
ALTER TABLE silver.silver_shops 
ADD CONSTRAINT fk_silver_shops_city 
FOREIGN KEY (city_id) 
REFERENCES silver.silver_cities(city_id);

-- Employees -> Cities
ALTER TABLE silver.silver_employees 
ADD CONSTRAINT fk_silver_employees_city 
FOREIGN KEY (city_id) 
REFERENCES silver.silver_cities(city_id);

-- Employees -> Shops
ALTER TABLE silver.silver_employees 
ADD CONSTRAINT fk_silver_employees_shop 
FOREIGN KEY (shop_id) 
REFERENCES silver.silver_shops(shop_id);

-- Customers -> Cities
ALTER TABLE silver.silver_customers 
ADD CONSTRAINT fk_silver_customers_city 
FOREIGN KEY (city_id) 
REFERENCES silver.silver_cities(city_id);

-- Sales -> Employees
ALTER TABLE silver.silver_sales 
ADD CONSTRAINT fk_silver_sales_employee 
FOREIGN KEY (employee_id) 
REFERENCES silver.silver_employees(employee_id);

-- Sales -> Customers
ALTER TABLE silver.silver_sales 
ADD CONSTRAINT fk_silver_sales_customer 
FOREIGN KEY (customer_id) 
REFERENCES silver.silver_customers(customer_id);

-- Sales -> Products
ALTER TABLE silver.silver_sales 
ADD CONSTRAINT fk_silver_sales_product 
FOREIGN KEY (product_id) 
REFERENCES silver.silver_products(product_id);

-- Sales -> Shops (enrichment)
ALTER TABLE silver.silver_sales 
ADD CONSTRAINT fk_silver_sales_shop 
FOREIGN KEY (shop_id) 
REFERENCES silver.silver_shops(shop_id);

-- Sales -> Cities (enrichment)
ALTER TABLE silver.silver_sales 
ADD CONSTRAINT fk_silver_sales_city 
FOREIGN KEY (city_id) 
REFERENCES silver.silver_cities(city_id);

-- BUSINESS LOGIC CONSTRAINTS

-- Employees: hire_date must be after birth_date
ALTER TABLE silver.silver_employees 
ADD CONSTRAINT chk_employee_hire_after_birth 
CHECK (hire_date > birth_date);

-- Sales: quantity must be positive
ALTER TABLE silver.silver_sales 
ADD CONSTRAINT chk_sales_quantity_positive 
CHECK (quantity >= 0);

-- Sales: total_price must be positive
ALTER TABLE silver.silver_sales 
ADD CONSTRAINT chk_sales_total_price_positive 
CHECK (total_price >= 0);

-- Sales: discount between 0 and 100
ALTER TABLE silver.silver_sales 
ADD CONSTRAINT chk_sales_discount_range 
CHECK (discount >= 0 AND discount <= 100);

-- Products: price must be positive
ALTER TABLE silver.silver_products 
ADD CONSTRAINT chk_product_price_positive 
CHECK (price >= 0);

-- VERIFICATION

-- Show all constraints
SELECT 
    conname as constraint_name,
    contype as constraint_type,
    pg_get_constraintdef(c.oid) as constraint_definition
FROM pg_constraint c
JOIN pg_namespace n ON n.oid = c.connamespace
WHERE n.nspname = 'silver'
ORDER BY contype, conname;

-- Check business constraint violations (should be 0)
SELECT 
    'Employees with hire_date <= birth_date' as check_type,
    COUNT(*) as violations
FROM silver.silver_employees
WHERE hire_date <= birth_date
UNION ALL
SELECT 
    'Sales with negative quantity',
    COUNT(*)
FROM silver.silver_sales
WHERE quantity < 0
UNION ALL
SELECT 
    'Sales with negative price',
    COUNT(*)
FROM silver.silver_sales
WHERE total_price < 0
UNION ALL
SELECT 
    'Sales with invalid discount',
    COUNT(*)
FROM silver.silver_sales
WHERE discount < 0 OR discount > 100;

COMMIT;


SELECT 
    'Constraints successfully applied!' as status;

