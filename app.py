from flask import Flask, render_template, request, redirect, url_for, g, flash
from cars.database import CarDatabase
from cars.car import Car
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", 'fallback-dev-secret-key')


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
    # Home page - display all cars with statistics
    db = get_db()
    cars = db.get_all_cars()
    
    # Calculate statistics
    total_cars = len(cars)
    total_value = sum(car.price for _, car in cars) if cars else 0
    avg_price = total_value / total_cars if total_cars > 0 else 0
    newest_year = max((car.year for _, car in cars), default=0) if cars else 0
    oldest_year = min((car.year for _, car in cars), default=0) if cars else 0
    
    stats = {
        'total_cars': total_cars,
        'total_value': total_value,
        'avg_price': avg_price,
        'newest_year': newest_year,
        'oldest_year': oldest_year
    }
    
    return render_template('index.html', cars=cars, stats=stats)


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

        flash(f'✅ {brand} {model} added successfully!', 'success')
        
        # Redirect to home
        return redirect(url_for('index'))
    
    # GET request - show form
    return render_template('add_car.html')

@app.route('/delete/<int:car_id>')
def delete_car(car_id):
    # Delete car by ID
    db = get_db()

    flash('🗑️ Car deleted successfully!', 'success')

    db.delete_car(car_id)
    return redirect(url_for('index'))

@app.route('/edit/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    # Edit car page
    db = get_db()

    if request.method == 'POST':
        # Get form data
        brand = request.form['brand']
        model = request.form['model']
        year = int(request.form['year'])
        price = float(request.form['price'])

        # Update car in database
        # First delete the old car
        db.delete_car(car_id)
        # Then add the updated car
        car = Car(brand, model, year, price)
        db.add_car(car)

        flash(f'✏️ {brand} {model} updated successfully!', 'success')
        return redirect(url_for('index'))
    
    # GET request - show form with current car data
    all_cars = db.get_all_cars()
    current_car = None
    for cid, car in all_cars:
        if cid == car_id:
            current_car = car
            break

    if current_car is None:
        flash('❌ Car not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template('edit_car.html', car=current_car, car_id=car_id)

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

# Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    flash('❌ Something went wrong! Please try again later.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)