from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b8e2fa0e4c74d9:d8f543d8@us-cluster-east-01.k8s.cleardb.net/heroku_6c38564e8dba3e8'
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
    data = request.get_json()
    new_income = Income(
        source=data['source'],
        amount=data['amount'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date()
    )
    db.session.add(new_income)
    db.session.commit()
    return jsonify({'message': 'Income added', 'income': {'source': new_income.source}})

@app.route('/income/<int:id>', methods=['PUT'])
def edit_income(id):
    data = request.get_json()
    income = Income.query.get(id)
    if income:
        income.source = data['source']
        income.amount = data['amount']
        income.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        db.session.commit()
        return jsonify({'message': 'Income updated'})
    return jsonify({'message': 'Income not found'}), 404

@app.route('/income/<int:id>', methods=['DELETE'])
def delete_income(id):
    income = Income.query.get(id)
    if income:
        db.session.delete(income)
        db.session.commit()
        return jsonify({'message': 'Income deleted'})
    return jsonify({'message': 'Income not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
