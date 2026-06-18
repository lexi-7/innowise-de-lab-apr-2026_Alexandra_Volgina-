-- Enable transaction for atomic cleanup
BEGIN;

-- REMOVE DUPLICATES FROM EMPLOYEES

WITH duplicate_employees AS (
    SELECT 
        employee_id,
        COUNT(*) as dup_count,
        ARRAY_AGG(employee_id ORDER BY employee_id) as ids
    FROM silver.silver_employees
    GROUP BY employee_id
    HAVING COUNT(*) > 1
)
DELETE FROM silver.silver_employees
WHERE employee_id IN (
    SELECT DISTINCT employee_id 
    FROM duplicate_employees
)
AND employee_id NOT IN (
    SELECT MIN(employee_id)
    FROM silver.silver_employees
    GROUP BY employee_id
    HAVING COUNT(*) > 1
);

-- Show remaining duplicates (should be 0)
SELECT 
    'Remaining duplicates' as check_type,
    employee_id,
    COUNT(*) as duplicate_count
FROM silver.silver_employees
GROUP BY employee_id
HAVING COUNT(*) > 1;

-- HANDLE NULL KEYS

-- Remove employees with NULL employee_id
DELETE FROM silver.silver_employees
WHERE employee_id IS NULL;

-- Remove sales with NULL foreign keys
DELETE FROM silver.silver_sales
WHERE employee_id IS NULL 
   OR customer_id IS NULL 
   OR product_id IS NULL;

-- CLEAN ORPHAN RECORDS

-- Remove employees with no sales
DELETE FROM silver.silver_employees
WHERE employee_id NOT IN (
    SELECT DISTINCT employee_id 
    FROM silver.silver_sales 
    WHERE employee_id IS NOT NULL
);

-- Remove customers with no sales
DELETE FROM silver.silver_customers
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id 
    FROM silver.silver_sales 
    WHERE customer_id IS NOT NULL
);

-- Remove products with no sales
DELETE FROM silver.silver_products
WHERE product_id NOT IN (
    SELECT DISTINCT product_id 
    FROM silver.silver_sales 
    WHERE product_id IS NOT NULL
);

-- Update sales with shop_id and city_id

-- Update missing shop_id from employees
UPDATE silver.silver_sales s
SET shop_id = e.shop_id
FROM silver.silver_employees e
WHERE s.employee_id = e.employee_id
  AND (s.shop_id IS NULL OR s.shop_id = 0);

-- Update missing city_id from employees
UPDATE silver.silver_sales s
SET city_id = e.city_id
FROM silver.silver_employees e
WHERE s.employee_id = e.employee_id
  AND (s.city_id IS NULL OR s.city_id = 0);

-- VERIFICATION 

-- Check NULL values in sales enrichment fields
SELECT 
    'NULL check: shop_id' as check_type,
    COUNT(*) as null_count
FROM silver.silver_sales
WHERE shop_id IS NULL OR shop_id = 0
UNION ALL
SELECT 
    'NULL check: city_id' as check_type,
    COUNT(*) as null_count
FROM silver.silver_sales
WHERE city_id IS NULL OR city_id = 0;

-- Show enrichment coverage
SELECT 
    'Enrichment coverage' as metric,
    COUNT(*) as total_sales,
    COUNT(CASE WHEN shop_id IS NOT NULL AND shop_id > 0 THEN 1 END) as has_shop,
    COUNT(CASE WHEN city_id IS NOT NULL AND city_id > 0 THEN 1 END) as has_city
FROM silver.silver_sales;

-- Check date validity
SELECT 
    'Invalid hire dates' as check_type,
    COUNT(*) as count
FROM silver.silver_employees
WHERE hire_date <= birth_date;

COMMIT;

-- FINAL VERIFICATION AFTER COMMIT

-- Show final row counts
SELECT 
    'silver_countries' as table_name,
    COUNT(*) as row_count
FROM silver.silver_countries
UNION ALL
SELECT 'silver_cities', COUNT(*) FROM silver.silver_cities
UNION ALL
SELECT 'silver_categories', COUNT(*) FROM silver.silver_categories
UNION ALL
SELECT 'silver_products', COUNT(*) FROM silver.silver_products
UNION ALL
SELECT 'silver_shops', COUNT(*) FROM silver.silver_shops
UNION ALL
SELECT 'silver_employees', COUNT(*) FROM silver.silver_employees
UNION ALL
SELECT 'silver_customers', COUNT(*) FROM silver.silver_customers
UNION ALL
SELECT 'silver_sales', COUNT(*) FROM silver.silver_sales
ORDER BY table_name;

