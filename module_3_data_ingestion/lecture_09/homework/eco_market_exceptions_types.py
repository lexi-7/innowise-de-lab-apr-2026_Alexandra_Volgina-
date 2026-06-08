from typing import Optional, Union, List, Tuple, Dict
from decimal import Decimal, InvalidOperation

# TASK 1

def calculate_purchase(product_name: str, weight: any, price: float) -> None:
    """
    Safely calculate purchase cost with error handling for invalid input data.
    
    Parameters:
    product_name (str): Name of the product
    weight (any): Weight of the batch (will be converted to float)
    price (float): Price per kg
    
    Returns:
    None: Function prints results or errors to console
    
    This function handles:
    - TypeError: When wrong type is used in calculations
    - ValueError: When string cannot be converted to float
    - ZeroDivisionError: When weight is zero
    """
    try:
        # Attempt to convert weight to float
        numeric_weight: float = float(weight)
        
        # Calculate total cost
        total_cost: float = numeric_weight * price
        
        # Calculate technical index (this can cause ZeroDivisionError)
        technical_index: float = 100 / numeric_weight
        
        # If all calculations succeed, display results
        print(f"Товар: {product_name}. Итоговая стоимость: {total_cost}$")
        
    except ValueError as e:
        print(f"Тип ошибки: {type(e)}")
        print(f"Сообщение: {e}")
        
    except ZeroDivisionError as e:
        print(f"Тип ошибки: {type(e)}")
        print(f"Сообщение: {e}")
        
    except TypeError as e:
        print(f"Тип ошибки: {type(e)}")
        print(f"Сообщение: {e}")
        
    finally:
        print("--- Проверка партии завершена ---\n")

# Test Task 1 with different scenarios
print("TASK 1: Exception Handling")

# Test case 1: Correct data
calculate_purchase("Томаты", 100, 2.5)

# Test case 2: Value error (string instead of number)
calculate_purchase("Огурцы", "пятьдесят", 1.8)

# Test case 3: Zero division error (weight is zero)
calculate_purchase("Перец", 0, 4)

# Test case 4: Type error (list instead of number)
calculate_purchase("Зелень", [10], 5)

# TASK 2

def calculate_total_delivery_cost(
    product_name: str,
    weights: Union[List[float], Tuple[float, ...]],
    prices: Union[List[float], Tuple[float, ...]],
    discount: Optional[float] = None,
    currency_rate: Union[int, float] = 1,
    *extra_costs: float
) -> Dict[str, float]:
    """
    Calculate total delivery cost with type safety and comprehensive error checking.
    
    Parameters:
    product_name (str): Name of the product/batch
    weights (Union[List[float], Tuple[float, ...]]): Collection of weights for each item
    prices (Union[List[float], Tuple[float, ...]]): Collection of prices per kg for each item
    discount (Optional[float]): Discount percentage (0-1), None means no discount
    currency_rate (Union[int, float]): Currency conversion rate (default: 1)
    *extra_costs (float): Variable number of additional costs (shipping, packaging, etc.)
    
    Returns:
    Dict[str, float]: Dictionary with product name as key and total cost as value
    
    Raises:
    ValueError: If lengths of weights and prices don't match
    
    Example:
    >>> calculate_total_delivery_cost("Test", [100, 50], [4, 6], 0.1, 1, 20, 15)
    {'Test': 665.0}
    """
    # Type hints for local variables
    total_sum: float = 0.0
    discount_sum: float = 0.0
    extra_sum: float = 0.0
    final_sum: float = 0.0
    position_cost: float = 0.0
    
    # Validate that collections have the same length
    if len(weights) != len(prices):
        raise ValueError(f"Weights count ({len(weights)}) must match prices count ({len(prices)})")
    
    # Calculate total sum of all positions
    for i in range(len(weights)):
        position_cost = weights[i] * prices[i]
        total_sum += position_cost
    
    # Apply discount if provided
    if discount is not None:
        discount_sum = total_sum * (1 - discount)
    else:
        discount_sum = total_sum
    
    # Add all extra costs
    extra_sum = sum(extra_costs)
    
    # Calculate final sum with currency rate
    final_sum = (discount_sum + extra_sum) * currency_rate
    
    # Return dictionary with product name and final cost
    return {product_name: final_sum}


# Test Task 2 with provided data
print("\nTASK 2: Typed Function with Complex Logic")

# Test case 1: Vegetables batch
vegetable_result: Dict[str, float] = calculate_total_delivery_cost(
    "Овощная партия",  # product_name
    [100, 50],         # weights
    [4, 6],            # prices
    0.1,               # discount
    1,                 # currency_rate
    20, 15             # *extra_costs
)

for product, cost in vegetable_result.items():
    print(f"Товар: {product}, итоговая стоимость: {cost}")

# Test case 2: Fruits batch
fruit_result: Dict[str, float] = calculate_total_delivery_cost(
    "Фруктовая партия",
    (30, 20, 10),
    (15, 12, 18),
    None,
    1.2,
    25
)

for product, cost in fruit_result.items():
    print(f"Товар: {product}, итоговая стоимость: {cost}")


# Additional demonstration of type checking
print("TYPE HINTS DEMONSTRATION")

# Show the types of variables used
demo_weights: Tuple[float, ...] = (30, 20, 10)
demo_prices: List[float] = [15.0, 12.0, 18.0]
demo_discount: Optional[float] = None
demo_rate: Union[int, float] = 1.2

print(f"Demo weights type: {type(demo_weights)} with values: {demo_weights}")
print(f"Demo prices type: {type(demo_prices)} with values: {demo_prices}")
print(f"Demo discount type: {type(demo_discount)}")
print(f"Demo currency rate type: {type(demo_rate)}")

# Demonstrate the function with different parameter combinations
print("\nAdditional test cases:")

# Test with no discount and no extra costs
simple_result = calculate_total_delivery_cost(
    "Простая партия",
    [200],
    [3.5],
    discount=None,
    currency_rate=1
)
print(f"Simple batch (no discount, no extras): {simple_result}")

# Test with discount but no extra costs
discounted_result = calculate_total_delivery_cost(
    "Со скидкой",
    [100, 200],
    [5, 4],
    discount=0.15,
    currency_rate=1
)
print(f"Discounted batch: {discounted_result}")

# Test with multiple extra costs
extra_costs_result = calculate_total_delivery_cost(
    "С доп. расходами",  # product_name
    [50, 75],            # weights
    [10, 8],             # prices
    0.05,                # discount
    1.1,                 # currency_rate
    10, 25, 15, 30       # *extra_costs
)
print(f"Batch with multiple extras: {extra_costs_result}")
