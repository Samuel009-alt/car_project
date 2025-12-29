class Car: 
    def __init__(self, brand, model, year, price):
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
    
    def get_info(self):
        return f"{self.year} {self.brand} {self.model} - ${self.price:,.2f}"
    
    def apply_discount(self, percent):
        # Reduce price by a percentage
        discount =  self.price * (percent / 100)
        self.price -= discount
    
    def get_age(self):
        # Calculate car's age in years
        from datetime import datetime
        current_year = datetime.now().year
        return current_year - self.year 
    
    def is_vintage(self):
        # Check if car is vintage (25+ years old)
        return self.get_age() >= 25


# Test our Car class
if __name__ == "__main__":
    # Create car objects
    car1 = Car("Toyota", "Camry", 2022, 25000)
    car2 = Car("Ford", "Mustang", 1969, 45000)

    # Display car info
    print(car1.get_info())
    print(car2.get_info())

    # Test get_age method
    print(f"\nThe Mustang is {car2.get_age()} years old.")

    # Test apply_discount method
    print(f"\nOriginal Camry price: ${car1.price:,.2f}")
    car1.apply_discount(10)  # Apply 10% discount
    print(f"After 10% discount: ${car1.price:,.2f}")