from flask import Flask, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import os
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your models here
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/export', methods=['GET'])
def export_data():
    try:
        expenses = Expense.query.all()
        incomes = Income.query.all()

        # Define the CSV file path
        csv_file_path = 'exported_data.csv'

        # Write to CSV file
        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['ID', 'Category/Source', 'Amount', 'Date'])

            for expense in expenses:
                csvwriter.writerow([expense.id, expense.category, expense.amount, expense.date])

            for income in incomes:
                csvwriter.writerow([income.id, income.source, income.amount, income.date])

        return send_file(csv_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007)
