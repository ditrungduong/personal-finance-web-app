from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
# This configuration specifies the database URI and disables track modifications to save resources
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b8e2fa0e4c74d9:d8f543d8@us-cluster-east-01.k8s.cleardb.net/heroku_6c38564e8dba3e8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object and bind it to the Flask app
db = SQLAlchemy(app)

# Initialize Flask-Migrate to handle database migrations
migrate = Migrate(app, db)

# Define a model (a Python class) for the 'Income' table in the database
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    source = db.Column(db.String(100), nullable=False)  # Source of income (string, required)
    amount = db.Column(db.Float, nullable=False)  # Amount of income (float, required)
    date = db.Column(db.Date, nullable=False)  # Date of income (date, required)

# Define a route for the root URL
@app.route('/')
def index():
    return render_template('index.html')  # Render the 'index.html' template

# Define a route to display all incomes
@app.route('/income')
def income():
    incomes = Income.query.all()  # Query all Income records from the database
    return render_template('income.html', incomes=incomes)  # Render the 'income.html' template with the incomes data

# Define a route to handle adding a new income (POST request)
@app.route('/income', methods=['POST'])
def add_income():
    data = request.get_json()  # Get JSON data from the request
    new_income = Income(
        source=data['source'],  # Set the source from the request data
        amount=data['amount'],  # Set the amount from the request data
        date=datetime.strptime(data['date'], '%Y-%m-%d').date()  # Parse and set the date from the request data
    )
    db.session.add(new_income)  # Add the new income record to the database session
    db.session.commit()  # Commit the session to save the new income record to the database
    return jsonify({'message': 'Income added', 'income': {'source': new_income.source}})  # Return a JSON response

# Define a route to handle updating an existing income (PUT request)
@app.route('/income/<int:id>', methods=['PUT'])
def edit_income(id):
    data = request.get_json()  # Get JSON data from the request
    income = Income.query.get(id)  # Get the income record by id from the database
    if income:
        income.source = data['source']  # Update the source from the request data
        income.amount = data['amount']  # Update the amount from the request data
        income.date = datetime.strptime(data['date'], '%Y-%m-%d').date()  # Parse and update the date from the request data
        db.session.commit()  # Commit the session to save the updates to the database
        return jsonify({'message': 'Income updated'})  # Return a JSON response
    return jsonify({'message': 'Income not found'}), 404  # Return a 404 response if the income was not found

# Define a route to handle deleting an existing income (DELETE request)
@app.route('/income/<int:id>', methods=['DELETE'])
def delete_income(id):
    income = Income.query.get(id)  # Get the income record by id from the database
    if income:
        db.session.delete(income)  # Delete the income record from the database session
        db.session.commit()  # Commit the session to delete the income record from the database
        return jsonify({'message': 'Income deleted'})  # Return a JSON response
    return jsonify({'message': 'Income not found'}), 404  # Return a 404 response if the income was not found

# Run the app if this script is executed
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get the port from the environment or default to 5000
    app.run(debug=True, host='0.0.0.0', port=port)  # Run the app with debugging enabled
