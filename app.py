from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('CLEARDB_DATABASE_URL') or 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/income')
def income():
    incomes = Income.query.all()
    return render_template('income.html', incomes=incomes)

@app.route('/income', methods=['POST'])
def add_income():
    data = request.get_json()
    new_income = Income(source=data['source'], amount=data['amount'], date=data['date'])
    db.session.add(new_income)
    db.session.commit()
    return jsonify({'message': 'Income added', 'income': {'source': new_income.source, 'amount': new_income.amount, 'date': new_income.date}})

@app.route('/income/<int:id>', methods=['PUT'])
def update_income(id):
    data = request.get_json()
    income = Income.query.get(id)
    if income is None:
        return jsonify({'message': 'Income not found'}), 404
    income.source = data['source']
    income.amount = data['amount']
    income.date = data['date']
    db.session.commit()
    return jsonify({'message': 'Income updated'})

@app.route('/income/<int:id>', methods=['DELETE'])
def delete_income(id):
    income = Income.query.get(id)
    if income is None:
        return jsonify({'message': 'Income not found'}), 404
    db.session.delete(income)
    db.session.commit()
    return jsonify({'message': 'Income deleted'})

@app.route('/expenses')
def expenses():
    return render_template('expenses.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
