# Внешние ключи (FK)

## sales

- **employee_id** → ссылается на `employee_id` в таблице `employees`
- **customer_id** → ссылается на `customer_id` в таблице `customers`
- **product_id** → ссылается на `product_id` в таблице `products`

## shops

- **city_id** → ссылается на `city_id` в таблице `cities`

## cities

- **country_id** → ссылается на `country_id` в таблице `countries`

## employees

- **shop_id** → ссылается на `shop_id` в таблице `shops`
- **city_id** → ссылается на `city_id` в таблице `cities` 

## products

- **category_id** → ссылается на `category_id` в таблице `categories`

## customers

- **city_id** → ссылается на `city_id` в таблице `cities`