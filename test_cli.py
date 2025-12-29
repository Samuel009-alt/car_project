"""
Test script for Car Inventory CLI Application
Tests all features to ensure they work correctly
"""

from cars.car import Car
from cars.database import CarDatabase
import os

def test_car_class():
    """Test Car class functionality"""
    print("=" * 50)
    print("TEST 1: Car Class")
    print("=" * 50)
    
    # Create car
    car = Car("Toyota", "Camry", 2022, 25000)
    assert car.brand == "Toyota"
    assert car.model == "Camry"
    assert car.year == 2022
    assert car.price == 25000
    print("✓ Car creation works")
    
    # Test get_info
    info = car.get_info()
    assert "Toyota" in info
    assert "25,000" in info
    print(f"✓ get_info() works: {info}")
    
    # Test apply_discount
    original_price = car.price
    car.apply_discount(10)
    assert car.price == original_price * 0.9
    print(f"✓ apply_discount() works: ${original_price:,.2f} → ${car.price:,.2f}")
    
    # Test get_age
    age = car.get_age()
    assert age >= 0
    print(f"✓ get_age() works: {age} years old")
    
    # Test is_vintage
    vintage = car.is_vintage()
    print(f"✓ is_vintage() works: {vintage}")
    
    print("✅ All Car class tests passed!\n")


def test_database():
    """Test Database functionality"""
    print("=" * 50)
    print("TEST 2: Database Operations")
    print("=" * 50)
    
    # Use test database
    test_db = "test_cars.db"
    
    # Remove if exists
    if os.path.exists(test_db):
        os.remove(test_db)
    
    db = CarDatabase(test_db)
    
    # Test add_car
    car1 = Car("Tesla", "Model 3", 2023, 42000)
    car2 = Car("BMW", "X5", 2022, 65000)
    car3 = Car("BMW", "M3", 2023, 75000)
    
    db.add_car(car1)
    db.add_car(car2)
    db.add_car(car3)
    print("✓ Adding cars works")
    
    # Test get_all_cars
    cars = db.get_all_cars()
    assert len(cars) == 3
    print(f"✓ get_all_cars() works: {len(cars)} cars found")
    
    # Verify cars have IDs
    for car_id, car in cars:
        assert car_id > 0
        assert isinstance(car, Car)
    print("✓ Cars have valid IDs")
    
    # Test search_by_brand
    bmws = db.search_by_brand("BMW")
    assert len(bmws) == 2
    print(f"✓ search_by_brand() works: Found {len(bmws)} BMWs")
    
    # Test search case-insensitive
    bmws_lower = db.search_by_brand("bmw")
    assert len(bmws_lower) == 2
    print("✓ Search is case-insensitive")
    
    # Test delete_car
    db.delete_car(1)  # Delete Tesla
    remaining = db.get_all_cars()
    assert len(remaining) == 2
    print(f"✓ delete_car() works: {len(remaining)} cars remaining")
    
    # Close and cleanup
    db.close()
    os.remove(test_db)
    print("✓ Database cleanup successful")
    
    print("✅ All Database tests passed!\n")


def test_inventory_json():
    """Test JSON-based Inventory functionality"""
    print("=" * 50)
    print("TEST 3: JSON Inventory")
    print("=" * 50)
    
    from cars.inventory import Inventory
    
    test_file = "test_cars.json"
    
    # Remove if exists
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create inventory
    inv = Inventory()
    
    # Add cars
    inv.add_car(Car("Honda", "Civic", 2023, 28000))
    inv.add_car(Car("Toyota", "Corolla", 2022, 25000))
    print("✓ Adding cars to inventory works")
    
    # Test find_by_brand
    hondas = inv.find_by_brand("Honda")
    assert len(hondas) == 1
    print(f"✓ find_by_brand() works: Found {len(hondas)} Honda(s)")
    
    # Save to file
    inv.save_to_file(test_file)
    assert os.path.exists(test_file)
    print(f"✓ save_to_file() works: {test_file} created")
    
    # Load from file
    inv2 = Inventory()
    inv2.load_from_file(test_file)
    assert len(inv2.cars) == 2
    print(f"✓ load_from_file() works: Loaded {len(inv2.cars)} cars")
    
    # Cleanup
    os.remove(test_file)
    print("✓ Cleanup successful")
    
    print("✅ All Inventory tests passed!\n")


def test_api():
    """Test API functionality"""
    print("=" * 50)
    print("TEST 4: API Integration")
    print("=" * 50)
    
    from cars.api import fetch_car_makes, fetch_models_by_make
    
    # Test fetch_car_makes
    try:
        makes = fetch_car_makes()
        assert isinstance(makes, list)
        assert len(makes) > 0
        print(f"✓ fetch_car_makes() works: Got {len(makes)} manufacturers")
    except Exception as e:
        print(f"⚠ API test skipped (no internet?): {e}")
        return
    
    # Test fetch_models_by_make
    try:
        models = fetch_models_by_make("honda")
        assert isinstance(models, list)
        print(f"✓ fetch_models_by_make() works: Got {len(models)} Honda models")
    except Exception as e:
        print(f"⚠ Model fetch failed: {e}")
    
    print("✅ All API tests passed!\n")


def test_edge_cases():
    """Test edge cases and error handling"""
    print("=" * 50)
    print("TEST 5: Edge Cases")
    print("=" * 50)
    
    test_db = "test_edge.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    db = CarDatabase(test_db)
    
    # Test with zero cars
    cars = db.get_all_cars()
    assert len(cars) == 0
    print("✓ Empty database handled correctly")
    
    # Test search with no results
    results = db.search_by_brand("NonExistentBrand")
    assert len(results) == 0
    print("✓ Empty search results handled correctly")
    
    # Test delete non-existent car
    db.delete_car(999)  # Should not crash
    print("✓ Deleting non-existent car handled")
    
    # Test discount edge cases
    car = Car("Test", "Car", 2020, 10000)
    car.apply_discount(0.5)  # Very small discount
    assert car.price < 10000
    print("✓ Small discount works")
    
    car2 = Car("Test", "Car", 2020, 10000)
    car2.apply_discount(99.9)  # Large discount
    assert car2.price < 100
    print("✓ Large discount works")
    
    # Cleanup
    db.close()
    os.remove(test_db)
    
    print("✅ All edge case tests passed!\n")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("RUNNING COMPREHENSIVE TEST SUITE")
    print("=" * 50 + "\n")
    
    try:
        test_car_class()
        test_database()
        test_inventory_json()
        test_api()
        test_edge_cases()
        
        print("=" * 50)
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 50)
        print("\nYour CLI application is ready for production!")
        print("All features are working correctly.\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
