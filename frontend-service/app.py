from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object and bind it to the Flask app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Default admin credentials
admin_username = 'admin'

# Ensure an admin user exists
def create_admin_user():
    admin_password = 'admin'  # This should be set securely
    if not User.query.filter_by(username=admin_username).first():
        hashed_password = generate_password_hash(admin_password, method='sha256')
        new_user = User(username=admin_username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

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
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('index'))  # Redirect to index page after successful login
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')  # Render the 'login.html' template

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match. Please try again.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error: Username already exists.')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the user session
    return redirect(url_for('login'))  # Redirect to login page

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables for the data models
        create_admin_user()  # Ensure an admin user exists
    port = int(os.environ.get('PORT', 5000))  # Get the port from the environment or default to 5000
    app.run(debug=True, host='0.0.0.0', port=port)  # Run the app with debugging enabled
