from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/income.html')
def income():
    return render_template('income.html')

@app.route('/expenses.html')
def expenses():
    return render_template('expenses.html')
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
