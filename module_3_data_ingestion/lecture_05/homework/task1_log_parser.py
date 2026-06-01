# task1_log_parser.py
# Задание 1: Парсинг строки из лога кассы

# Входные данные
raw_log = "ORDER-2025-01-15|FRT-APPLE-PL|+111 (23) 456-78-90| мИНсК "

# 1. Разделение строки на части
order_id, product_code, raw_phone, raw_city = raw_log.split("|")

# 2. Разбор кода товара
# Получаем первые 3 символа (категория)
category = product_code[:3]

# Получаем последние 2 символа (регион) - используем отрицательные индексы
region = product_code[-2:]

# Находим позицию первого дефиса
first_dash_position = product_code.find("-")
print(f"Позиция первого дефиса в коде товара: {first_dash_position}")

# Проверяем, начинается ли код с "FRT"
if product_code.startswith("FRT"):
    print("Код товара начинается с 'FRT'")
else:
    print("Код товара не начинается с 'FRT'")

# 3. Очистка номера телефона (оставляем только цифры)
clean_phone = ""
for char in raw_phone:
    if char.isdigit():
        clean_phone += char

print(f"Длина номера телефона: {len(clean_phone)}")

# 4. Нормализация названия города
# Удаляем пробелы по краям, приводим к нижнему регистру, делаем первую букву заглавной
clean_city = raw_city.strip().lower().title()

# 5. Формирование итогового отчета
report = f"""Заказ: {order_id}
Категория: {category} | Регион: {region}
Телефон: {clean_phone}
Город: {clean_city}"""

print(report)
