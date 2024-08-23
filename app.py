from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuring SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

from datetime import datetime

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, company, email, message):
        self.name = name
        self.company = company
        self.email = email
        self.message = message
        self.date_submitted = datetime.utcnow()


# Create the database
with app.app_context():
    db.create_all()

@app.route('/form')
def index():
    return render_template('form.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form['name']
    company = request.form['company']
    email = request.form['email']
    message = request.form['message']

    # Store form data in the database
    new_contact = Contact(name=name, company=company, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()

    flash('Form submitted successfully!', 'success')
    return redirect('/')

@app.route('/')
def dashboard():
    contacts = Contact.query.all()
    return render_template('dashboard.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)
