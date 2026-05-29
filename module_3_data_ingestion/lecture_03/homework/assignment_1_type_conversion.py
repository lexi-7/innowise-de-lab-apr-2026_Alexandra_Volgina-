"""
Assignment 1: Type Conversion and Collections
EcoMarket Data Processing
"""

# 1. Initialize input variables
raw_sku = "CARROT-001"
raw_regions = ("Minsk", "Warsaw", "Berlin", "Warsaw")
raw_weight_str = "2.5"
raw_stock_str = "150"

# 2. Explicit type conversion
weight_kg = float(raw_weight_str)
stock_quantity = int(raw_stock_str)

# 3. Collection transformations
sku_as_list = list(raw_sku)
regions_list = list(raw_regions)
unique_regions = set(raw_regions)
regions_tuple = tuple(unique_regions)

# 4. Create empty collections (two ways each)
# Lists
empty_list_1 = []
empty_list_2 = list()

# Dictionaries
empty_dict_1 = {}
empty_dict_2 = dict()

# Tuples
empty_tuple_1 = ()
empty_tuple_2 = tuple()

# Sets (only one way - {} is empty dict, not set)
empty_set = set()

# 5. Check emptiness with bool()
print("=== Empty Collections Truth Values ===")
print(f"empty_list_1: {bool(empty_list_1)}")
print(f"empty_dict_1: {bool(empty_dict_1)}")
print(f"empty_tuple_1: {bool(empty_tuple_1)}")
print(f"empty_set: {bool(empty_set)}")

# Create non-empty collections
non_empty_list = [1, 2, 3]
non_empty_dict = {"key": "value"}
non_empty_tuple = (1, 2, 3)
non_empty_set = {1, 2, 3}

print("\n=== Non-Empty Collections Truth Values ===")
print(f"non_empty_list: {bool(non_empty_list)}")
print(f"non_empty_dict: {bool(non_empty_dict)}")
print(f"non_empty_tuple: {bool(non_empty_tuple)}")
print(f"non_empty_set: {bool(non_empty_set)}")

# 6. Print all values with their types
print("\n=== Converted Values ===")
print(f"{weight_kg} {type(weight_kg)}")
print(f"{stock_quantity} {type(stock_quantity)}")

print("\n=== Converted Collections ===")
print(f"{sku_as_list} {type(sku_as_list)}")
print(f"{regions_list} {type(regions_list)}")
print(f"{unique_regions} {type(unique_regions)}")
print(f"{regions_tuple} {type(regions_tuple)}")