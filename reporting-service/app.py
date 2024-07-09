from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime, timedelta
import plotly.express as px
import pandas as pd

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@db/personal_finance_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

def create_charts(time_period):
    end_date = datetime.now()
    
    if time_period == 'month':
        start_date = end_date - timedelta(days=30)
    elif time_period == '3_month':
        start_date = end_date - timedelta(days=90)
    elif time_period == '6_month':
        start_date = end_date - timedelta(days=180)
    elif time_period == '9_month':
        start_date = end_date - timedelta(days=270)
    elif time_period == 'year':
        start_date = end_date - timedelta(days=365)
    else:
        start_date = end_date - timedelta(days=30)  # Default to 1 month
    
    incomes = Income.query.filter(Income.date.between(start_date, end_date)).all()
    expenses = Expense.query.filter(Expense.date.between(start_date, end_date)).all()

    # Data processing
    income_data = pd.DataFrame([(i.source, i.amount, i.date) for i in incomes], columns=['Source', 'Amount', 'Date'])
    expense_data = pd.DataFrame([(e.category, e.amount, e.date) for e in expenses], columns=['Category', 'Amount', 'Date'])

    # Total Income vs Expense Bar Chart
    total_income = income_data['Amount'].sum()
    total_expense = expense_data['Amount'].sum()
    fig1 = px.bar(x=['Income', 'Expense'], y=[total_income, total_expense], title='Total Income vs Total Expense')

    # Pie Chart for Income
    income_pie = income_data.groupby('Source', as_index=False)['Amount'].sum()
    fig2 = px.pie(income_pie, values='Amount', names='Source', title='Income Sources')

    # Pie Chart for Expense
    expense_pie = expense_data.groupby('Category', as_index=False)['Amount'].sum()
    fig3 = px.pie(expense_pie, values='Amount', names='Category', title='Expense Categories')

    return fig1.to_html(full_html=False), fig2.to_html(full_html=False), fig3.to_html(full_html=False)

@app.route('/report')
def report():
    time_period = request.args.get('time_period', 'month')
    bar_chart, income_pie_chart, expense_pie_chart = create_charts(time_period)
    return render_template('report.html', bar_chart=bar_chart, income_pie_chart=income_pie_chart, expense_pie_chart=expense_pie_chart, selected_time_period=time_period)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(debug=True, host='0.0.0.0', port=port)
