from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b8e2fa0e4c74d9:d8f543d8@us-cluster-east-01.k8s.cleardb.net/heroku_6c38564e8dba3e8?reconnect=true'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/income')
def income():
    return render_template('income.html')

@app.route('/expenses')
def expenses():
    return render_template('expenses.html')

@app.route('/test_db')
def test_db():
    try:
        # Attempt to connect to the database
        db.session.execute('SELECT 1')
        return 'Database connection is working!'
    except Exception as e:
        return f'Error: {e}'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
