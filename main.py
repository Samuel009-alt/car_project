from cars.car import Car
from cars.database import CarDatabase

def show_menu():
    # Display menu options
    print("\n===== Car Inventory Menu =====")
    print("1. Add a car")
    print("2. View all cars")
    print("3. Search cars by brand")
    print("4. Filter by year")
    print("5. Filter by price range")
    print("6. Delete a car")
    print("0. Exit")
    print("==============================")

def add_car(db):
    # Get car details from user
    print("\n--- Add a New Car ---")
    brand = input("Brand: ")
    model = input("Model: ")
    year = input("Year: ")
    price = input("Price: ")

    # Validate and save 
    try:
        car = Car(brand, model, int(year), float(price))
        db.add_car(car)
    except ValueError:
        print("Invalid year or price. Please enter valid values.")

def view_all_cars(db):
    # Display all cars
    print("\n--- All Cars in Inventory ---")
    cars = db.get_all_cars()
    if not cars:
        print("No cars found in inventory.")
        return
    for car_id, car in cars:
        print(f"ID {car_id}: {car.get_info()}")

def search_by_brand(db):
    # Search cars by brand
    print("\n--- Search Cars by Brand ---")
    brand = input("Enter brand: ")
    cars = db.search_by_brand(brand)
    if not cars:
        print(f"No cars found for '{brand}'")
        return
    for car in cars:
        print(car.get_info())

def filter_by_year(db):
    # Filter cars by year 
    print("\n--- Filter Cars by Year ---")
    year = input("Enter year: ")

    try:
        year = int(year)
        cars = db.get_all_cars()
        filtered = [(car_id, car) for car_id, car in cars if car.year == year]
        if not filtered:
            print(f"No cars found from year {year}")
            return
        for car_id, car in filtered:
            print(f"ID {car_id}: {car.get_info()}")
    except ValueError:
        print("Invalid year. Please enter a valid number.")

def filter_by_price(db):
    # Filter cars by price range 
    print("\n--- Filter Cars by Price Range ---")
    min_price = input("Enter minimum price: ")
    max_price = input("Enter maximum price: ")

    try:
        min_price = float(min_price)
        max_price = float(max_price)
        cars = db.get_all_cars()
        filtered = [(car_id, car) for car_id, car in cars if min_price <= car.price <= max_price]

        if not filtered:
            print(f"No cars found between ${min_price:,.2f} and ${max_price:,.2f}")
            return
        for car_id, car in filtered:
            print(f"ID {car_id}: {car.get_info()}")
    except ValueError:
        print("Invalid price. Please enter valid numbers.")

def delete_car(db):
    # Delete a car by ID
    print("\n--- Delete a Car ---")
    view_all_cars(db)
    car_id = input("\nEnter car ID to delete: ")

    try:
        db.delete_car(int(car_id))
    except ValueError:
        print("Invalid ID. Please enter a valid number.")

def main():
    # Main program loop
    db = CarDatabase("cars.db")

    while True:
        show_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            add_car(db)
        elif choice == "2":
            view_all_cars(db)
        elif choice == "3":
            search_by_brand(db)
        elif choice == "4":
            filter_by_year(db)
        elif choice == "5":
            filter_by_price(db)
        elif choice == "6":
            delete_car(db)
        elif choice == "0":
            print("Goodbye!")
            db.close()
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()