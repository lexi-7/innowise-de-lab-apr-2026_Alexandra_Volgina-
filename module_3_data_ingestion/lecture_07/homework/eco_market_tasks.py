import json

# TASK 1

print("TASK 1: Central Warehouse Coordinates")


# Create a tuple with warehouse coordinates
center_coords = (40.7128, -74.0060)

# Attempt to modify the tuple (this will cause an error)
# The following line is commented because it raises TypeError
# center_coords[0] = 41.0000  # TypeError: 'tuple' object does not support item assignment

# Display coordinates using index access
print(f"Coordinates of the location of the central warehouse: {center_coords[0]} , {center_coords[1]}")

# Check variable type
print(type(center_coords))

# Check tuple length
print(len(center_coords))

# TASK 2

print("TASK 2: Product Card Update")

# Create the product dictionary
product = {
    "id": 105,
    "name": "Organic Buckwheat",
    "price": 3.50,
    "stock": 100
}

# Modify existing key
product["price"] = 4.20

# Add new key-value pair
product["category"] = "Grains"

# Safely retrieve a key using .get() (returns 0 if key doesn't exist)
discount_rate = product.get("discount", 0)

# Display results
print(product)
print(discount_rate)

# TASK 3

print("TASK 3: Unique Suppliers Identification")

# Create the suppliers log list
suppliers_log = [
    "FreshFarm Inc",
    "GreenFields Ltd",
    "AgroWorld Co",
    "FreshFarm Inc",
    "GreenFields Ltd"
]

# Convert to set to get unique suppliers
unique_suppliers = set(suppliers_log)

# Try to add an existing supplier (won't duplicate)
unique_suppliers.add("GreenFields Ltd")

# Check if a supplier exists in the set
is_freshfarm_present = "FreshFarm Inc" in unique_suppliers

# Display results
print(is_freshfarm_present)
print(unique_suppliers)
print(len(unique_suppliers))

# TASK 4

print("TASK 4: Currency Conversion USD to EUR")

# Create USD prices dictionary
usd_prices = {
    "Banana": 1.2,
    "Mango": 2.5,
    "Avocado": 2.0
}

# Use dictionary comprehension to convert to EUR (exchange rate: 0.9)
eur_prices = {fruit: price * 0.9 for fruit, price in usd_prices.items()}

# Display result
print(eur_prices)

# TASK 5

print("TASK 5: API Response Processing with JSON")

# Define JSON string (API response)
api_response_json = """
{
    "store": "StoreHub",
    "orders": [
        {"id": 1, "total": 50},
        {"id": 2, "total": 200},
        {"id": 3, "total": 150}
    ]
}
"""

# Deserialize JSON string to Python dictionary
data = json.loads(api_response_json)

# Get orders list
orders = data["orders"]

# Filter high-value orders (total > 100) using list comprehension
high_value_orders = [order for order in orders if order["total"] > 100]

# Add filtered list to dictionary
data["high_value_orders"] = high_value_orders

# Serialize updated dictionary back to JSON string
updated_json = json.dumps(data, indent=4)

# Display result
print(updated_json)
