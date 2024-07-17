from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@db/personal_finance_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object and bind it to the Flask app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/update-password', methods=['GET', 'POST'])
def update_password():
    if request.method == 'POST':
        username = 'admin'  # Default username
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, old_password):
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password updated successfully.')
            return redirect(url_for('update_password'))
        else:
            flash('Old password is incorrect. Please try again.')
            return redirect(url_for('update_password'))

    return render_template('update_password.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the user session
    return redirect(url_for('login'))  # Redirect to login page

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))  # Get the port from the environment or default to 5004
    app.run(debug=True, host='0.0.0.0', port=port)  # Run the app with debugging enabled
