SELECT 
    s.sales_id,
    p.product_name,
    sh.address AS shop_address
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN employees e ON s.employee_id = e.employee_id
JOIN shops sh ON e.shop_id = sh.shop_id
ORDER BY s.sales_id
LIMIT 10;

SELECT 
    sh.shop_id,
    sh.address,
    c.city_name,
    co.country_name AS country
FROM shops sh
JOIN cities c ON sh.city_id = c.city_id
JOIN countries co ON c.country_id = co.country_id
WHERE co.country_name = 'Poland';

SELECT 
    s.sales_id,
    p.product_name,
    s.total_price,
    p.class,
    s.customer_id,
    s.sales_timestamp
FROM sales s
JOIN products p ON s.product_id = p.product_id
WHERE s.total_price > 1500 
    AND p.class = 'B'
ORDER BY s.sales_id
LIMIT 10;

SELECT 
    co.country_name AS country,
    COUNT(sh.shop_id) AS number_of_shops
FROM shops sh
JOIN cities c ON sh.city_id = c.city_id
JOIN countries co ON c.country_id = co.country_id
GROUP BY co.country_name
ORDER BY number_of_shops DESC;

SELECT 
    p.product_id,
    p.product_name,
    SUM(s.total_price) AS total_revenue,
    AVG(s.total_price) AS avg_sale
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_id, p.product_name
HAVING SUM(s.total_price) > 400000
ORDER BY total_revenue DESC;

SELECT 
    e.first_name,
    e.last_name,
    sh.address AS address,
    s.total_price AS max_amount
FROM sales s
JOIN employees e ON s.employee_id = e.employee_id
JOIN shops sh ON e.shop_id = sh.shop_id
WHERE s.total_price = (SELECT MAX(total_price) FROM sales);

WITH monthly_revenue AS (
    SELECT 
        DATE_TRUNC('month', TO_TIMESTAMP(s.sales_timestamp, 'YYYY-MM-DD HH24:MI:SS')) AS sale_month,
        SUM(s.total_price) AS monthly_revenue
    FROM sales s
    JOIN employees e ON s.employee_id = e.employee_id
    JOIN shops sh ON e.shop_id = sh.shop_id
    JOIN cities c ON sh.city_id = c.city_id
    JOIN countries co ON c.country_id = co.country_id
    WHERE co.country_name = 'Germany'
        AND s.sales_timestamp IS NOT NULL
        AND s.sales_timestamp != ''
    GROUP BY DATE_TRUNC('month', TO_TIMESTAMP(s.sales_timestamp, 'YYYY-MM-DD HH24:MI:SS'))
),
monthly_with_previous AS (
    SELECT 
        sale_month,
        monthly_revenue,
        LAG(monthly_revenue) OVER (ORDER BY sale_month) AS previous_month_revenue
    FROM monthly_revenue
)
SELECT 
    sale_month,
    monthly_revenue,
    previous_month_revenue,
    monthly_revenue - previous_month_revenue AS difference_from_previous_month
FROM monthly_with_previous
WHERE previous_month_revenue IS NOT NULL
ORDER BY sale_month;

WITH shop_stats AS (
    SELECT 
        sh.shop_id,
        sh.address,
        co.country_name AS country,
        COUNT(s.sales_id) AS total_sales_count,
        SUM(s.total_price) AS total_sales_amount
    FROM shops sh
    JOIN cities c ON sh.city_id = c.city_id
    JOIN countries co ON c.country_id = co.country_id
    JOIN employees e ON sh.shop_id = e.shop_id
    JOIN sales s ON e.employee_id = s.employee_id
    WHERE s.sales_timestamp IS NOT NULL 
        AND s.sales_timestamp != ''
        AND s.total_price IS NOT NULL
    GROUP BY sh.shop_id, sh.address, co.country_name
    HAVING COUNT(s.sales_id) >= 2
),
country_totals AS (
    SELECT 
        country,
        SUM(total_sales_amount) AS country_total
    FROM shop_stats
    GROUP BY country
)
SELECT 
    ss.country,
    ss.shop_id,
    ss.address AS shop_address,
    ss.total_sales_count,
    ss.total_sales_amount,
    ct.country_total,
    ROUND((ss.total_sales_amount / ct.country_total)::NUMERIC, 10) AS country_sales_share,
    RANK() OVER (PARTITION BY ss.country ORDER BY ss.total_sales_amount DESC) AS shop_rank,
    SUM(ss.total_sales_amount) OVER (PARTITION BY ss.country ORDER BY ss.total_sales_amount DESC ROWS UNBOUNDED PRECEDING) AS country_running_total
FROM shop_stats ss
JOIN country_totals ct ON ss.country = ct.country
ORDER BY ss.country, shop_rank;


