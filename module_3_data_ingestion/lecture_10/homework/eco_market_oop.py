
# Parent Class: Product (Base Product)

class Product:
    """
    Base class representing a generic product in EcoMarket.
    Demonstrates encapsulation with private attribute __price.
    """
    
    def __init__(self, name: str, price: float):
        """
        Constructor for Product class.
        
        Parameters:
        name (str): Product name
        price (float): Product price (must be positive)
        """
        self.name = name
        self.__price = price  # Private attribute (encapsulation)
    
    def set_price(self, new_price: float) -> None:
        """
        Setter for price with validation.
        Only allows positive prices for security.
        
        Parameters:
        new_price (float): New price to set
        """
        if new_price > 0:
            self.__price = new_price
        else:
            print("Ошибка безопасности: Цена должна быть положительной!")
    
    def get_price(self) -> float:
        """
        Getter for price.
        
        Returns:
        float: Current product price
        """
        return self.__price
    
    def calculate_cost(self) -> float:
        """
        Calculate cost for base product.
        
        Returns:
        float: Product price
        """
        return self.get_price()
    
    def get_display_info(self) -> str:
        """
        Get display information for base product.
        
        Returns:
        str: Formatted product information
        """
        return f"Товар: {self.name} | Цена: {self.get_price()} руб."

# Child Class: WeighableProduct (Weight-based Product)

class WeighableProduct(Product):
    """
    Child class representing products sold by weight.
    Demonstrates inheritance and polymorphism.
    """
    
    def __init__(self, name: str, price: float, weight: float):
        """
        Constructor for WeighableProduct class.
        
        Parameters:
        name (str): Product name
        price (float): Price per kg
        weight (float): Weight in kilograms
        """
        super().__init__(name, price)  # Call parent constructor
        self.weight = weight
    
    def calculate_cost(self) -> float:
        """
        Calculate cost for weighable product.
        Overrides parent method (polymorphism).
        
        Returns:
        float: Price * weight
        """
        return self.get_price() * self.weight
    
    def get_display_info(self) -> str:
        """
        Get display information for weighable product.
        Overrides parent method (polymorphism).
        
        Returns:
        str: Formatted product information with weight and total cost
        """
        return f"Весовой товар: {self.name} | Вес: {self.weight} кг | Итого: {self.calculate_cost()} руб."

# Child Class: PackagedProduct (Packaged Product)

class PackagedProduct(Product):
    """
    Child class representing products sold in packages.
    Demonstrates inheritance and polymorphism.
    """
    
    def __init__(self, name: str, price: float, quantity: int):
        """
        Constructor for PackagedProduct class.
        
        Parameters:
        name (str): Product name
        price (float): Price per unit
        quantity (int): Number of units in package
        """
        super().__init__(name, price)  # Call parent constructor
        self.quantity = quantity
    
    def calculate_cost(self) -> float:
        """
        Calculate cost for packaged product.
        Overrides parent method (polymorphism).
        
        Returns:
        float: Price * quantity
        """
        return self.get_price() * self.quantity
    
    def get_display_info(self) -> str:
        """
        Get display information for packaged product.
        Overrides parent method (polymorphism).
        
        Returns:
        str: Formatted product information with quantity and total cost
        """
        return f"Упаковка: {self.name} | Количество: {self.quantity} шт. | Итого: {self.calculate_cost()} руб."

# Cash Register Simulation

def main():
    """
    Simulate cash register operation with shopping cart.
    Demonstrates encapsulation, inheritance, and polymorphism in action.
    """
    
    # Create empty shopping cart
    cart = []
    
    # Add products to cart
    milk = Product("Молоко", 100)
    apples = WeighableProduct("Яблоки", 50, 2.5)
    eggs = PackagedProduct("Яйца", 12, 10)
    
    cart.append(milk)
    cart.append(apples)
    cart.append(eggs)
    
    # Attempt to set negative price (security test)
    print("Попытка взлома системы:")
    milk.set_price(-200)
    print()
    
    # Display receipt
    print("Чек EcoMarket")
    
    total_cost = 0
    for item in cart:
        # Polymorphism in action - Python automatically calls the correct method
        print(item.get_display_info())
        total_cost += item.calculate_cost()
    
    print(f"ИТОГО К ОПЛАТЕ: {total_cost} руб.")


# Run the simulation
if __name__ == "__main__":
    main()

print("ДОПОЛНИТЕЛЬНАЯ ДЕМОНСТРАЦИЯ ООП")

# Demonstrate encapsulation (price is protected)
print("\n1. Инкапсуляция (Encapsulation):")
test_product = Product("Тестовый товар", 500)
print(f"   Цена через геттер: {test_product.get_price()} руб.")
# print(test_product.__price)  # This would raise AttributeError (private attribute)
print("   Прямой доступ к __price невозможен - данные защищены!")

# Demonstrate inheritance
print("\n2. Наследование (Inheritance):")
print(f"   WeighableProduct наследуется от Product: {issubclass(WeighableProduct, Product)}")
print(f"   PackagedProduct наследуется от Product: {issubclass(PackagedProduct, Product)}")

# Demonstrate polymorphism
print("\n3. Полиморфизм (Polymorphism):")
products = [
    Product("Хлеб", 50),
    WeighableProduct("Бананы", 80, 1.5),
    PackagedProduct("Сок", 95, 3)
]

for product in products:
    # Same method call produces different results based on object type
    print(f"   {product.get_display_info()}")

# Demonstrate secure price validation
print("\n4. Безопасность цен (Price Security):")
insecure_product = Product("Попытка взлома", 200)
print(f"   Исходная цена: {insecure_product.get_price()} руб.")
insecure_product.set_price(-999)  # Rejected
insecure_product.set_price(350)   # Accepted
print(f"   Цена после попытки взлома: {insecure_product.get_price()} руб.")
