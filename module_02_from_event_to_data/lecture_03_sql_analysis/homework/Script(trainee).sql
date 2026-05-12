--Задание 3: DCL (Управление доступом к данным)

SELECT * FROM sales LIMIT 5;


SELECT current_user;


INSERT INTO sales (employee_id, customer_id, product_id, quantity, discount, total_price, sales_timestamp, transaction_number)
VALUES (1, 1, 1, 1, 0, 10.99, NOW(), 'TRAINEE_TEST_2');


UPDATE sales SET discount = 5 WHERE transaction_number = 'TRAINEE_TEST_2';

DELETE FROM sales WHERE transaction_number = 'TRAINEE_TEST_2';