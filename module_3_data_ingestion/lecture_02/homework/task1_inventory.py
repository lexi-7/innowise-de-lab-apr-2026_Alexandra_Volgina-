# task1_inventory.py
# Задание 1: Обмен категорий продуктов и расчет стоимости с НДС

# Инициализация переменных с ошибочными значениями
category_a = "Vegetables"  # Ошибочно присвоено фруктам
category_b = "Fruits"      # Ошибочно присвоено овощам
price_per_unit_a = 150     # Цена за ящик фруктов
quantity_a = 40             # Количество ящиков фруктов
vat_rate = 0.2              # Ставка НДС 20%

# Обмен значений переменных (без временной переменной)
category_a, category_b = category_b, category_a

# Расчет общей стоимости партии с НДС
total_without_vat = price_per_unit_a * quantity_a
vat_amount = total_without_vat * vat_rate
total_value = total_without_vat + vat_amount

# Вывод результатов в консоль
print(f"Текущая категория A: {category_a}")
print(f"Общая стоимость партии с НДС: {total_value}")


