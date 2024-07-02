from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object and bind it to the Flask app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define a simple home route
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')  # Render the 'index.html' template
    return redirect(url_for('login'))  # Redirect to login page if not logged in

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # For demonstration, assume these are the valid credentials
        if username == 'admin' and password == 'password':
            session['username'] = username
            return redirect(url_for('index'))  # Redirect to index page after successful login
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')  # Render the 'login.html' template

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the user session
    return redirect(url_for('login'))  # Redirect to login page

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get the port from the environment or default to 5000
    app.run(debug=True, host='0.0.0.0', port=port)  # Run the app with debugging enabled
