# Классификация CSV-файлов и сущностей

## Сущности и их CSV-файлы

### Справочники

**countries** → countries.csv
- Содержит список стран
- Атрибуты: country_id, country_name, country_code

**cities** → cities.csv
- Содержит список городов с привязкой к странам
- Атрибуты: city_id, city_name, zipcode, country_id

**shops** → shops.csv
- Содержит информацию о магазинах
- Атрибуты: shop_id, city_id, address
- Каждый магазин расположен в определенном городе

**employees** → employees.csv
- Содержит информацию о сотрудниках
- Атрибуты: employee_id, first_name, middle_initial, last_name, birth_date, gender, city_id, shop_id, hire_date

**customers** → customers.csv
- Содержит информацию о покупателях
- Атрибуты: customer_id, first_name, middle_initial, last_name, city_id, address

**categories** → categories.csv
- Содержит категории продуктов
- Атрибуты: category_id, category_name
- Пример: Fruits, Vegetables, Meat & Poultry, Fish & Seafood

**products** → products.csv
- Содержит информацию о товарах
- Атрибуты: product_id, product_name, price, category_id, class, modify_timestamp, resistant, is_allergic, vitality_days

### Фактическая таблица – операции продаж

**sales** → sales.csv
- Содержит информацию о продажах
- Атрибуты: sales_id, employee_id, customer_id, product_id, quantity, discount, total_price, sales_timestamp, transaction_number
- Одна строка = одна позиция в чеке (отдельный товар в покупке)
- Размер: > 2 миллиона строк 

## Связи между сущностями

### Иерархия расположения:

**countries** (1) —— (∞) **cities**
- Одна страна содержит много городов

**cities** (1) —— (∞) **shops**
- Один город содержит много магазинов

**shops** (1) —— (∞) **employees**
- В одном магазине работает много сотрудников

### Категории и продукты:

**categories** (1) —— (∞) **products**
- Одна категория содержит много продуктов

**products** (1) —— (∞) **sales**
- Один продукт может быть продан много раз (в разных чеках)

### Продажи (факты):

**employees** (1) —— (∞) **sales**
- Один сотрудник может обслужить много продаж

**customers** (1) —— (∞) **sales**
- Один покупатель может совершить много покупок

**products** (1) —— (∞) **sales**
- Один продукт участвует во многих продажах

## Фиксируемые операции

### Основная операция: продажа товара
- Каждая строка в таблице sales - это одна позиция в чеке
- Фиксируется:
  - Кто продал (employee_id)
  - Кто купил (customer_id)
  - Что купил (product_id)
  - Сколько купил (quantity)
  - Цена со скидкой (total_price)
  - Размер скидки (discount)
  - Когда купил (sales_timestamp)
  - Номер чека/транзакции (transaction_number)

### Вспомогательные операции:
- Добавление новых продуктов
- Изменение цен
- Прием на работу сотрудников
- Добавление новых магазинов

## Ключевые атрибуты для связи

### Для products:
- **product_id** - первичный ключ (уникальный ID товара)
- **product_name** - название товара
- **price** - цена
- **category_id** - внешний ключ к categories

### Для employees:
- **employee_id** - первичный ключ (уникальный ID сотрудника)
- **first_name** + **last_name** - имя и фамилия
- **shop_id** - внешний ключ к shops (где работает)
- **hire_date** - дата найма

## Примечания

### Особенности:
1. **sales** - самая большая таблица (>2 млн строк), содержит историю всех продаж
2. **transaction_number** в sales может объединять несколько записей в один чек
3. **class** в products - вероятно, класс качества товара (A, B, C)
4. **vitality_days** - срок годности в днях
5. **resistant** и **is_allergic** - булевы поля (true/false)

### Возможное дублирование:
- У employees и customers есть city_id, хотя employee.city_id возможно избыточен, так как employee связан с shop, а shop связан с city. Это может быть город проживания а не работы