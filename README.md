# 🚗 Car Inventory Management System

A Python-based car inventory management system with both CLI and web interfaces (web interface coming soon).

## 📋 Features

### Current (CLI Version)
- ✅ Add cars to inventory
- ✅ View all cars with IDs
- ✅ Search cars by brand
- ✅ Filter cars by year
- ✅ Filter cars by price range
- ✅ Delete cars from inventory
- ✅ SQLite database for persistent storage

### Coming Soon
- 🔄 Web application interface (Flask)
- 🔄 Import car data from external API
- 🔄 Export inventory to JSON/CSV

## 🛠️ Technologies Used

- **Python 3.13**
- **SQLite3** - Database
- **urllib** - API requests
- **JSON** - Data serialization

## 📁 Project Structure

```
car-project/
├── main.py              # CLI application entry point
├── cars/                # Main package
│   ├── __init__.py      # Package initialization
│   ├── car.py           # Car class definition
│   ├── database.py      # Database operations
│   ├── inventory.py     # Inventory management (JSON-based)
│   └── api.py           # API integration functions
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Samuel009-alt/car_project.git
cd car_project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Run the CLI application:
```bash
python main.py
```

## 📖 Usage

### CLI Application

Run the main application:
```bash
python main.py
```

You'll see a menu with options:
1. **Add a car** - Enter brand, model, year, and price
2. **View all cars** - Display all cars in inventory with IDs
3. **Search cars by brand** - Find cars by manufacturer
4. **Filter by year** - Show cars from a specific year
5. **Filter by price range** - Find cars within a price range
6. **Delete a car** - Remove a car by its ID
0. **Exit** - Close the application

### Example

```
===== Car Inventory Menu =====
1. Add a car
2. View all cars
3. Search cars by brand
4. Filter by year
5. Filter by price range
6. Delete a car
0. Exit
==============================
Enter choice: 1

--- Add a New Car ---
Brand: Toyota
Model: Camry
Year: 2022
Price: 25000
Added: 2022 Toyota Camry - $25,000.00
```

## 🎓 Learning Journey

This project was built as a learning exercise covering:

### Phase 1: Core Python Concepts ✅
- Object-Oriented Programming (Classes & Objects)
- File Handling (JSON)
- Database Management (SQLite)
- API Integration
- User Input Validation
- Error Handling
- List Comprehensions

### Phase 2: Web Development (Coming Soon)
- Flask Framework
- HTML Templates
- Forms Handling
- RESTful Routes

## 📚 Code Examples

### Creating a Car Object

```python
from cars.car import Car

# Create a new car
car = Car("Toyota", "Camry", 2022, 25000)

# Get car information
print(car.get_info())  # Output: 2022 Toyota Camry - $25,000.00

# Apply discount
car.apply_discount(10)  # 10% off
print(f"New price: ${car.price:,.2f}")
```

### Working with the Database

```python
from cars.database import CarDatabase
from cars.car import Car

# Initialize database
db = CarDatabase("cars.db")

# Add a car
car = Car("Tesla", "Model 3", 2023, 42000)
db.add_car(car)

# Get all cars
cars = db.get_all_cars()
for car_id, car in cars:
    print(f"ID {car_id}: {car.get_info()}")

# Search by brand
results = db.search_by_brand("Tesla")

# Close database connection
db.close()
```

## 🤝 Contributing

This is a learning project, but suggestions and improvements are welcome!

## 📄 License

This project is open source and available for educational purposes.

## 👤 Author

**Samuel**
- GitHub: [@Samuel009-alt](https://github.com/Samuel009-alt)

## 🎯 Roadmap

- [x] CLI Application
- [ ] Flask Web Application
- [ ] User Authentication
- [ ] Car Images Upload
- [ ] Advanced Search Filters
- [ ] Export/Import Functionality
- [ ] API Documentation

---

Built with ❤️ as a Python learning project
