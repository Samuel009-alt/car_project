import urllib.request
import json

def fetch_car_makes():
    # Fetch list of car manufacturers from API
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            makes = data["Results"][:10] # Get first 10 
            return makes
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    
def fetch_models_by_make(make_name):
    # Fetch models for a specific car make
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make_name}?format=json"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            models = data["Results"][:5] # Get first 5
            return models
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    
# Test API
if __name__ == "__main__":
    print("=== Car Manufacturers ===")
    makes = fetch_car_makes()
    for make in makes:
        print(f"  {make['Make_Name']}")

    print("\n=== Honda Models ===")
    models = fetch_models_by_make("honda")
    for model in models:
        print(f"  {model['Model_Name']}")   