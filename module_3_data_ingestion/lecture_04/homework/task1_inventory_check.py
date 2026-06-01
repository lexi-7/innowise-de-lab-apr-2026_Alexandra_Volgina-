# task1_inventory_check.py

# Дан список товаров
products = ["Яблоки", "Хлеб", "Молоко", "Печенье", "Сок", "Кефир"]

# Выборочная проверка каждого второго товара
for i in range(0, len(products), 2):
    product_name = products[i]
    name_length = len(product_name)
    
    if product_name == "Бананы":
        print(f"Обнаружены бананы! Проверка прервана.")
        break
    
    print(f"Индекс {i}: Проверен товар {product_name} (Длина названия: {name_length} символов)")
else:
    print("--- Выборочная проверка успешно завершена ---")
