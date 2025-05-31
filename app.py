from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Traveler

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'  # Use a strong secret key for security
db.init_app(app)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the Booking page
@app.route('/booking')
def booking():
    return render_template('booking.html')

# Route for the Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        email = request.form['email']
        password = request.form['password']
        
        # Check credentials (you can replace with real db checks)
        if email == "user@example.com" and password == "password123":
            flash('Login successful!', 'success')
            session['user'] = email
            return redirect(url_for('dashboard'))  # Redirect to dashboard after login
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html')

# Route for the Dashboard page
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('You must be logged in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    return render_template('dashboard.html')

# Route for the Payment page
@app.route('/payment')
def payment():
    return render_template('payment.html')

# Route for the Notification page
@app.route('/notification')
def notification():
    return render_template('notification.html')

# Route for the Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Create a new Traveler object
        new_travel = Traveler(name=name, email=email, phone=phone)

        # Add the new traveler to the session and commit to the database
        db.session.add(new_travel)
        db.session.commit()

        # Flash a success message
        flash('Registration successful!', 'success')

        # Redirect to the booking page after registration
        return redirect(url_for('booking'))

    return render_template('register.html')

# Debugging: Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
