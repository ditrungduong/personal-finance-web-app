from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime
import logging

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object and bind it to the Flask app
db = SQLAlchemy(app)

# Initialize Flask-Migrate to handle database migrations
migrate = Migrate(app, db)

# Define a model (a Python class) for the 'Expense' table in the database
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    category = db.Column(db.String(100), nullable=False)  # Expense category (string, required)
    amount = db.Column(db.Float, nullable=False)  # Amount of expense (float, required)
    date = db.Column(db.Date, nullable=False)  # Date of expense (date, required)

# Define a route for the root URL
@app.route('/')
def index():
    return render_template('index.html')  # Render the 'index.html' template

# Define a route to display all expenses
@app.route('/expenses')
def expenses():
    expenses = Expense.query.all()  # Query all Expense records from the database
    return render_template('expenses.html', expenses=expenses)  # Render the 'expenses.html' template with the expenses data

# Define a route to handle adding a new expense (POST request)
@app.route('/expenses', methods=['POST'])
def add_expense():
    try:
        data = request.get_json()  # Get JSON data from the request
        new_expense = Expense(
            category=data['category'],  # Set the category from the request data
            amount=data['amount'],  # Set the amount from the request data
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()  # Parse and set the date from the request data
        )
        db.session.add(new_expense)  # Add the new expense record to the database session
        db.session.commit()  # Commit the session to save the new expense record to the database
        return jsonify({'message': 'Expense added', 'expense': {'category': new_expense.category}}), 201  # Return a JSON response
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding expense: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Define a route to handle updating an existing expense (PUT request)
@app.route('/expenses/<int:id>', methods=['PUT'])
def edit_expense(id):
    try:
        data = request.get_json()
        expense = Expense.query.get(id)
        if expense:
            expense.category = data['category']
            expense.amount = data['amount']
            expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            db.session.commit()
            return jsonify({'message': 'Expense updated'}), 200
        return jsonify({'message': 'Expense not found'}), 404
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating expense with id {id}: {e}")
        return jsonify({'error': str(e)}), 500

# Define a route to handle deleting an existing expense (DELETE request)
@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    try:
        expense = Expense.query.get(id)  # Get the expense record by id from the database
        if expense:
            db.session.delete(expense)  # Delete the expense record from the database session
            db.session.commit()  # Commit the session to delete the expense record from the database
            return jsonify({'message': 'Expense deleted'}), 200  # Return a JSON response with HTTP 200 status
        return jsonify({'message': 'Expense not found'}), 404  # Return a 404 response if the expense was not found
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting expense: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Run the app if this script is executed
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))  # Get the port from the environment or default to 5002
    app.run(debug=True, host='0.0.0.0', port=port)  # Run the app with debugging enabled
