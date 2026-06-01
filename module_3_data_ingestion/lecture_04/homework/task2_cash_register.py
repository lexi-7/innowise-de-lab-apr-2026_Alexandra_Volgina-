# task2_cash_register.py

daily_logs = [
    [500, 0, 1200],
    [300, -999, 800],
    [1500, 200]
]

total_revenue = 0

for cash_index, transactions in enumerate(daily_logs, start=1):
    print(f"\n--- Обработка Кассы №{cash_index} ---")
    
    for transaction in transactions:
        if transaction == -999:
            print("Аварийная остановка кассы!")
            break
        
        if transaction == 0:
            print("Сбой (0).")
            continue
        
        if transaction > 0:
            total_revenue += transaction
            print(f"Добавлено: {transaction}")

print(f"\n=== ИТОГ ДНЯ ===")
print(f"Общая выручка магазина: {total_revenue}")
