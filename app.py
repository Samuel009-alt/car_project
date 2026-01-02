from flask import Flask, render_template, request, redirect, url_for, g
from cars.database import CarDatabase
from cars.car import Car

# Create Flask app
app = Flask(__name__)


def get_db():
    # Get database connection for current request
    if 'db' not in g:
        g.db = CarDatabase("cars.db")
    return g.db


@app.teardown_appcontext
def close_db(error):
    # Close database connection at end of request
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    # Home page - display all cars
    db = get_db()
    cars = db.get_all_cars()
    return render_template('index.html', cars=cars)


@app.route('/add', methods=['GET', 'POST'])
def add_car():
    # Add car page
    if request.method == 'POST':
        # Get form data
        brand = request.form['brand']
        model = request.form['model']
        year = int(request.form['year'])
        price = float(request.form['price'])
        
        # Create and save car
        db = get_db()
        car = Car(brand, model, year, price)
        db.add_car(car)
        
        # Redirect to home
        return redirect(url_for('index'))
    
    # GET request - show form
    return render_template('add_car.html')

@app.route('/delete/<int:car_id>')
def delete_car(car_id):
    # Delete car by ID
    db = get_db()
    db.delete_car(car_id)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Search and filter page
    db = get_db()
    results = []
    search_performed = False

    if request.method == 'POST':
        search_performed = True
        search_type = request.form.get('search_type')

        if search_type == 'brand':
            # Search by brand
            brand = request.form['brand']
            results = db.search_by_brand(brand)
            # Convert to same format as get_all_cars (with IDs)
            results = [(None, car) for car in results]

        elif search_type == 'year':
            # Filter by year
            year = int(request.form['year'])
            all_cars = db.get_all_cars()
            results = [(car_id, car) for car_id, car in all_cars if car.year == year]

        elif search_type == 'price':
            # Filter by price range
            min_price = float(request.form['min_price'])
            max_price = float(request.form['max_price'])
            all_cars = db.get_all_cars()
            results = [(car_id, car) for car_id, car in all_cars if min_price <= car.price <= max_price]

    return render_template('search.html', results=results, search_performed=search_performed)

if __name__ == '__main__':
    app.run(debug=True)