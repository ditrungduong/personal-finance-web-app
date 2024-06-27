from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('CLEARDB_DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_income', methods=['POST'])
def add_income():
    source = request.json['source']
    amount = request.json['amount']
    date = request.json['date']
    new_income = Income(source=source, amount=amount, date=date)
    db.session.add(new_income)
    db.session.commit()
    return jsonify({"message": "Income added successfully!"})

@app.route('/add_expense', methods=['POST'])
def add_expense():
    description = request.json['description']
    amount = request.json['amount']
    date = request.json['date']
    new_expense = Expense(description=description, amount=amount, date=date)
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully!"})

@app.route('/incomes', methods=['GET'])
def get_incomes():
    incomes = Income.query.all()
    result = [
        {"source": income.source, "amount": income.amount, "date": income.date.strftime('%Y-%m-%d')}
        for income in incomes
    ]
    return jsonify(result)

@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    result = [
        {"description": expense.description, "amount": expense.amount, "date": expense.date.strftime('%Y-%m-%d')}
        for expense in expenses
    ]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
