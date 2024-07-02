from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime
import logging

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@db/personal_finance_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object and bind it to the Flask app
db = SQLAlchemy(app)

# Initialize Flask-Migrate to handle database migrations
migrate = Migrate(app, db)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define a model (a Python class) for the 'Income' table in the database
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    source = db.Column(db.String(100), nullable=False)  # Source of income (string, required)
    amount = db.Column(db.Float, nullable=False)  # Amount of income (float, required)
    date = db.Column(db.Date, nullable=False)  # Date of income (date, required)

# Define a route for the root URL
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')  # Render the 'index.html' template
    return redirect(url_for('login'))  # Redirect to login page if not logged in

# Define a route to display all incomes
@app.route('/income')
def income():
    try:
        incomes = Income.query.all()  # Query all Income records from the database
        return render_template('income.html', incomes=incomes)  # Render the 'income.html' template with the incomes data
    except Exception as e:
        logging.error(f"Error fetching incomes: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Define a route to handle adding a new income (POST request)
@app.route('/income', methods=['POST'])
def add_income():
    try:
        data = request.get_json()  # Get JSON data from the request
        new_income = Income(
            source=data['source'],  # Set the source from the request data
            amount=data['amount'],  # Set the amount from the request data
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()  # Parse and set the date from the request data
        )
        db.session.add(new_income)  # Add the new income record to the database session
        db.session.commit()  # Commit the session to save the new income record to the database
        return jsonify({'message': 'Income added', 'income': {'source': new_income.source}}), 201  # Return a JSON response
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding income: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Define a route to handle updating an existing income (PUT request)
@app.route('/income/<int:id>', methods=['PUT'])
def edit_income(id):
    try:
        data = request.get_json()
        income = Income.query.get(id)
        if income:
            income.source = data['source']
            income.amount = data['amount']
            income.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            db.session.commit()
            return jsonify({'message': 'Income updated'}), 200
        return jsonify({'message': 'Income not found'}), 404
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating income with id {id}: {e}")
        return jsonify({'error': str(e)}), 500

# Define a route to handle deleting an existing income (DELETE request)
@app.route('/income/<int:id>', methods=['DELETE'])
def delete_income(id):
    try:
        income = Income.query.get(id)  # Get the income record by id from the database
        if income:
            db.session.delete(income)  # Delete the income record from the database session
            db.session.commit()  # Commit the session to delete the income record from the database
            return jsonify({'message': 'Income deleted'}), 200  # Return a JSON response with HTTP 200 status
        return jsonify({'message': 'Income not found'}), 404  # Return a 404 response if the income was not found
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting income: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Define a route to handle user login (GET and POST requests)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # For demonstration, assume these are the valid credentials
        if username == 'admin' and password == 'password':
            session['username'] = username
            return redirect(url_for('index'))  # Redirect to index page after successful login
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')  # Render the 'login.html' template

# Define a route to handle user logout
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the user session
    return redirect(url_for('login'))  # Redirect to login page

# Run the app if this script is executed
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Get the port from the environment or default to 5001
    app.run(debug=True, host='0.0.0.0', port=port)  # Run the app with debugging enabled
