from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object and bind it to the Flask app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define a simple home route
@app.route('/')
def index():
    return render_template('index.html')  # Render the 'index.html' template

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get the port from the environment or default to 5000
    app.run(debug=True, host='0.0.0.0', port=port)  # Run the app with debugging enabled
