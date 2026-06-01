# task2_data_normalization.py
# Задание 2: Подготовка данных к загрузке в систему

# Входные данные
product = " фермерский ТВОРОГ "
price = 4.567
qty = 3
csv_row = "milk,bread,cheese"
review = "Это лучший ТВОРОГ в городе!"
file_path = r"C:\EcoMarket\data\2025\january\sales.csv"

# 1. Нормализация названия товара
# Удаляем лишние пробелы, приводим к нижнему регистру, делаем каждое слово с заглавной буквы
clean_product = product.strip().lower().title()

# 2. Формирование чека для клиента
total = price * qty

# Формируем чек с использованием \n для переноса строк и \t для табуляции
receipt = f'Чек "EcoMarket"\n\tТовар: {clean_product}\n\tКол-во: {qty}\n\tИтого: {total:.2f} руб.'

print(receipt)

# 3. Подготовка строки из CSV
# Разделяем строку по запятой и объединяем через " | "
csv_items = csv_row.split(",")
formatted_csv = " | ".join(csv_items)
print(formatted_csv)

# 4. Проверка отзыва клиента
# Проверяем содержится ли слово "творог" без учета регистра
if "творог" in review.lower():
    print("Отзыв относится к категории: Dairy")

# 5. Работа с путём к файлу
# Выводим путь к файлу (raw-строка сохраняет обратные слеши)
print(file_path)

# Объяснение использования raw-строки (r"") в комментарии ниже
