# TASK 1

# Global constant (approved by finance department)
SMALL_BATCH_LIMIT = 500

def calculate_batch(weight, price, discount=0.0):
    """
    Calculate total batch cost and check if it exceeds the small batch limit.
    
    Parameters:
    weight (float): Weight of the batch in kg
    price (float): Price per kg in USD
    discount (float, optional): Seasonal discount percentage (default: 0.0)
    
    Returns:
    tuple: (final_sum, is_limit_exceeded) where final_sum is the total cost
           and is_limit_exceeded is a boolean flag
    
    Example:
    >>> calculate_batch(100, 4)
    (400.0, False)
    >>> calculate_batch(50, 20, 0.10)
    (900.0, True)
    """
    total_sum = weight * price * (1 - discount)
    is_limit_exceeded = total_sum > SMALL_BATCH_LIMIT
    return (total_sum, is_limit_exceeded)

# Test Task 1
print("TASK 1: Batch Cost Calculator")

# Batch 1: Carrots (100kg at $4/kg, no discount)
carrot_sum, carrot_exceeded = calculate_batch(100, 4)
print(f"Партия 1 (Морковь): Сумма {carrot_sum}. Превышение лимита: {carrot_exceeded}")

# Batch 2: Apples (50kg at $20/kg, 10% discount)
apple_sum, apple_exceeded = calculate_batch(50, 20, discount=0.10)
print(f"Партия 2 (Яблоки): Сумма {apple_sum}. Превышение лимита: {apple_exceeded}")

print("\n")

# TASK 2

def audit_logger(func):
    """
    Decorator that logs the execution of a function.
    
    Parameters:
    func: The function to be decorated
    
    Returns:
    wrapper: The wrapped function with logging capability
    
    This decorator prints audit messages before and after function execution
    without modifying the original function's logic.
    """
    def wrapper(*args, **kwargs):
        print("[AUDIT] Запуск анализа....")
        result = func(*args, **kwargs)
        print("[AUDIT] Анализ завершен.")
        return result
    return wrapper

@audit_logger
def get_sorted_report(branches):
    """
    Sort branches by revenue in descending order.
    
    Parameters:
    branches (list): List of dictionaries containing branch data
                    Each dict must have 'city' and 'revenue' keys
    
    Returns:
    list: Sorted list of branches by revenue (highest to lowest)
    
    Uses lambda function as the key for sorting by revenue.
    """
    return sorted(branches, key=lambda branch: branch["revenue"], reverse=True)

# Input data for Task 2
branches = [
    {"city": "Minsk", "revenue": 15000},
    {"city": "Warsaw", "revenue": 32000},
    {"city": "London", "revenue": 12000}
]

# Test Task 2
print("TASK 2: Audit Logger with Sorting Report")

# Call the decorated function
sorted_branches = get_sorted_report(branches)

# Display formatted results
print("Топ филиалов:")
for i, branch in enumerate(sorted_branches, 1):
    print(f"{i}. {branch['city']}: {branch['revenue']}")

