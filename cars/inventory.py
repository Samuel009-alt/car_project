from .car import Car

class Inventory: 
    def __init__(self):
        # List to store all cars
        self.cars = []

    def add_car(self, car):
        # Add a Car object to the inventory
        self.cars.append(car)

    def list_cars(self):
        # Display all cars
        if not self.cars:
            print("No cars in inventory.")
            return
        for i, car in enumerate(self.cars, 1):
            print(f"{i}. {car.get_info()}")

    def find_by_brand(self, brand):
        # Find all cars matching a brand
        results = []
        for car in self.cars:
            if car.brand.lower() == brand.lower():
                results.append(car)
        return results
    
    def remove_car(self, index):
        # Remove car by its position (1-based index)
        if 1 <= index <= len(self.cars):
            removed = self.cars.pop(index - 1)
            print(f"Removed: {removed.get_info()}")
        else:
            print("Invalid index. No car removed.")

    def save_to_file(self, filename):
        # Save inventory to a JSON file
        import json
        data = []
        for car in self.cars:
            data.append({
                'brand': car.brand,
                'model': car.model,
                'year': car.year,
                'price': car.price
            })
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(self.cars)} cars to {filename}.")

    def load_from_file(self, filename):
        # Load inventory from a JSON file
        import json
        import os
        if not os.path.exists(filename):
            print(f"File {filename} not found.")
            return
        with open(filename, "r") as f:
            data = json.load(f)
        for item in data:
            car = Car(item["brand"], item["model"], item["year"], item["price"])
            self.add_car(car)
        print(f"Loaded {len(data)} cars from {filename}.")


# Test our Inventory class
if __name__ == "__main__":
    # Test loading from existing file
    print("=== Loading from cars.json ===")
    inv = Inventory()
    inv.load_from_file("cars.json")
    inv.list_cars()
    
    # Add a new car
    print("\n=== Adding a new car ===")
    inv.add_car(Car("Honda", "Civic", 2023, 28000))
    inv.list_cars()
    
    # Save updated inventory
    print("\n=== Saving updated inventory ===")
    inv.save_to_file("cars.json")
   