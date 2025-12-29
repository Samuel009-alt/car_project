import sqlite3
from .car import Car

class CarDatabase:
    def __init__(self, db_name):
        # Connect to database (creates file if not exists)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        # Create cars table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def add_car(self, car):
        # Insert a car into database
        self.cursor.execute(
            'INSERT INTO cars (brand, model, year, price) VALUES (?, ?, ?, ?)',
            (car.brand, car.model, car.year, car.price)
        )
        self.conn.commit()
        print(f"Added: {car.get_info()}")

    def get_all_cars(self):
        # Retrieve all cars from database
        self.cursor.execute('SELECT id, brand, model, year, price FROM cars')
        rows = self.cursor.fetchall()
        return [(row[0], Car(row[1], row[2], row[3], row[4])) for row in rows]
    
    def delete_car(self, car_id):
        # Delete a car by its ID
        self.cursor.execute('DELETE FROM cars WHERE id = ?', (car_id,))
        self.conn.commit()
        print(f"Deleted car with ID {car_id}")

    def search_by_brand(self, brand):
        # Find cars by brand
        self.cursor.execute(
            'SELECT brand, model, year, price FROM cars WHERE brand LIKE ?',
            (f'%{brand}%',)
        )
        rows = self.cursor.fetchall()
        return [Car(row[0], row[1], row[2], row[3]) for row in rows]

    def close(self):
        # Close the database connection
        self.conn.close()


# Test database
if __name__ == "__main__":
    db = CarDatabase("cars.db")

    # Add some cars
    db.add_car(Car("BMW", "M3", 2023, 75000))
    db.add_car(Car("BMW", "X5", 2022, 65000))
    db.add_car(Car("Audi", "A4", 2022, 45000))
    db.add_car(Car("Toyota", "Camry", 2021, 28000))

    # Get all cars
    print("\n=== All Cars ===")
    cars = db.get_all_cars()
    for car in cars:
        print(car.get_info())

    # Search by brand
    print("\n=== Search for BMW ===")
    bmws = db.search_by_brand("BMW")
    for car in bmws:
        print(car.get_info())

    # Delete a car with ID 3
    print("\n=== Deleting car ID 3 ===")
    db.delete_car(3)

    # Show remaining cars
    print("\n=== Remaining Cars ===")
    cars = db.get_all_cars()
    for car in cars:
        print(car.get_info())

    db.close()
