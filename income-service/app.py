from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime
import logging

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)
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
    try:
        data = request.get_json()
        new_income = Income(
            source=data['source'],
            amount=data['amount'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        )
        db.session.add(new_income)
        db.session.commit()
        return jsonify({'message': 'Income added', 'income': {'source': new_income.source}}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding income: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

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

@app.route('/income/<int:id>', methods=['DELETE'])
def delete_income(id):
    try:
        income = Income.query.get(id)
        if income:
            db.session.delete(income)
            db.session.commit()
            return jsonify({'message': 'Income deleted'}), 200
        return jsonify({'message': 'Income not found'}), 404
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting income: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
