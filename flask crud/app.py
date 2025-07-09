from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__) # Create a Flask application instance

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
db = SQLAlchemy(app) # Initialize the SQLAlchemy database instance

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary key
    name = db.Column(db.String(120), nullable=False) # Student name
    email = db.Column(db.String(120), nullable=False) # Student age
    contact = db.Column(db.Integer, nullable=False) # Student grade
    course = db.Column(db.String(50), nullable=False) # Student course
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        course = request.form['course']
        print (name, email, contact, course) # Print student details to console

        new_student = Student(name = name, email = email, contact = contact, course = course)
        db.session.add(new_student)
        db.session.commit() 

        return render_template('add.html') # Render the add.html template
    else:
        return render_template('add.html')
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create the database tables
        app.run(debug=True) # Run the Flask application in debug mode