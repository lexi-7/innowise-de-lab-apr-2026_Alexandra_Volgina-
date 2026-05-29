"""
Assignment 2: Business Rules with Logical Operators
EcoMarket Product Status Processing
"""

# 1. Initialize product variables
product_name = "Морковь мытая"
price = 2.5
stock_quantity = 150
is_local_farm = True
supplier = None

# Discount check variables
has_coupon = True
has_card = False
total = 10

# 2. Calculate is_hit based on business rule
# Rule: price < 3 AND is_local_farm is True
is_hit = price < 3 and is_local_farm

# 3. Display result
print(f"Является ли товар хитом? {is_hit}")

# 4. Additional business checks
has_supplier = supplier is not None
can_show_in_app = has_supplier and stock_quantity > 0
needs_restock = stock_quantity <= 20 or is_hit
is_blocked = not (is_local_farm)

# Display results
print(f"Поставщик указан? {has_supplier}")
print(f"Показывать в приложении? {can_show_in_app}")
print(f"Нужно пополнение? {needs_restock}")
print(f"Товар заблокирован для акции? {is_blocked}")

# 5. Operator precedence demonstration
# Rule: (has_coupon OR has_card) AND total > 50
discount_without_brackets = has_coupon or has_card and total > 50
discount_with_brackets = (has_coupon or has_card) and total > 50

print(f"\nСкидка без скобок: {discount_without_brackets}")
print(f"Скидка со скобками: {discount_with_brackets}")

# 6. Modify values with augmented assignment operators
# Increase price by 1.0
price += 1.0

# Double the stock quantity
stock_quantity *= 2

# Calculate full boxes of 10 kg
boxes = stock_quantity
boxes //= 10

print(f"\nЦена после изменения: {price}")
print(f"Остаток после изменения: {stock_quantity}")
print(f"Полных коробок по 10 кг: {boxes}")

# Recalculate key metrics after changes
is_hit_after = price < 3 and is_local_farm
needs_restock_after = stock_quantity <= 20 or is_hit_after

print(f"\nЯвляется ли товар хитом (после изменений)? {is_hit_after}")
print(f"Нужно пополнение (после изменений)? {needs_restock_after}")

#Demonstrate truthiness with different collections
print("\n=== Bonus: Truthiness Demo ===")
print(f"Empty string '': {bool('')}")
print(f"Non-empty string 'text': {bool('text')}")
print(f"Zero 0: {bool(0)}")
print(f"Non-zero 42: {bool(42)}")
print(f"None: {bool(None)}")