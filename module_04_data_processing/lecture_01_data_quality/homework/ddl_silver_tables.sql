CREATE SCHEMA IF NOT EXISTS silver;

-- DIMENSION TABLES

-- Countries dimension
CREATE TABLE IF NOT EXISTS silver.silver_countries (
    country_id INTEGER,
    country_name VARCHAR(100),
    country_code VARCHAR(10),
    -- Metadata
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cities dimension
CREATE TABLE IF NOT EXISTS silver.silver_cities (
    city_id INTEGER,
    city_name VARCHAR(100),
    zipcode VARCHAR(20),
    country_id INTEGER,
    -- Metadata
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories dimension
CREATE TABLE IF NOT EXISTS silver.silver_categories (
    category_id INTEGER,
    category_name VARCHAR(200),
    -- Metadata
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products dimension
CREATE TABLE IF NOT EXISTS silver.silver_products (
    product_id INTEGER,
    product_name VARCHAR(200),
    price NUMERIC(10, 2),  -- Using NUMERIC for exact decimal values
    category_id INTEGER,
    class VARCHAR(50),
    modify_timestamp TIMESTAMP,  -- Converted to proper TIMESTAMP
    resistant BOOLEAN,  -- Converted to BOOLEAN
    is_allergic BOOLEAN,  -- Converted to BOOLEAN
    vitality_days INTEGER,
    -- Metadata
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Shops dimension
CREATE TABLE IF NOT EXISTS silver.silver_shops (
    shop_id INTEGER,
    city_id INTEGER,
    address VARCHAR(500),
    -- Metadata
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employees dimension
CREATE TABLE IF NOT EXISTS silver.silver_employees (
    employee_id INTEGER,
    first_name VARCHAR(100),
    middle_initial VARCHAR(10),
    last_name VARCHAR(100),
    birth_date DATE,  -- Converted to proper DATE
    gender VARCHAR(10),
    city_id INTEGER,
    shop_id INTEGER,
    hire_date DATE,  -- Converted to proper DATE
    -- Metadata
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers dimension
CREATE TABLE IF NOT EXISTS silver.silver_customers (
    customer_id INTEGER,
    first_name VARCHAR(100),
    middle_initial VARCHAR(10),
    last_name VARCHAR(100),
    city_id INTEGER,
    address VARCHAR(500),
    -- Metadata
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FACT TABLE: Sales

CREATE TABLE IF NOT EXISTS silver.silver_sales (
    sales_id INTEGER,
    employee_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    quantity NUMERIC(10, 2),
    discount NUMERIC(10, 2),
    total_price NUMERIC(10, 2),
    sales_timestamp TIMESTAMP,  -- Converted to proper TIMESTAMP
    transaction_number VARCHAR(100),
    -- Enrichment fields (for faster analytics)
    shop_id INTEGER,  -- Added from employee
    city_id INTEGER,  -- Added from employee
    -- Metadata
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE INDEXES (

CREATE INDEX IF NOT EXISTS idx_silver_products_category ON silver.silver_products(category_id);
CREATE INDEX IF NOT EXISTS idx_silver_employees_shop ON silver.silver_employees(shop_id);
CREATE INDEX IF NOT EXISTS idx_silver_sales_employee ON silver.silver_sales(employee_id);
CREATE INDEX IF NOT EXISTS idx_silver_sales_customer ON silver.silver_sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_silver_sales_product ON silver.silver_sales(product_id);
CREATE INDEX IF NOT EXISTS idx_silver_sales_timestamp ON silver.silver_sales(sales_timestamp);

