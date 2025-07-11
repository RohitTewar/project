from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)  # Initialise app

# config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
db = SQLAlchemy(app)


# Database Table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary key
    name = db.Column(db.String(120), nullable=False) # Student name
    email = db.Column(db.String(120), nullable=False) # Student age
    contact = db.Column(db.Integer, nullable=False) # Student grade
    course = db.Column(db.String(50), nullable=False) # Student course

@app.route('/')
def index():
    # Fetch all students from the database and pass them to the template
    students = Student.query.all() 
    print(students) # Debugging line to check students
    return render_template('index.html', students = students)


@app.route('/add', methods = ['GET', 'POST'])
def add():
        if request.method == 'POST':
               name = request.form['name']
               email = request.form['email']
               contact = request.form['contact']
               course = request.form['course']
               print(name, email, contact, course)

               new_student = Student(name = name, email = email, contact = contact, course = course)
               db.session.add(new_student) # Add the new student to the session
               db.session.commit() # Save the new student to the database
               return render_template('add.html')

        else:
              return render_template('add.html')


# Delete Route
@app.route('/delete/<int:id>')
def deleteStudent(id):
    print(id)
    student = Student.query.get_or_404(id)
    print(student)
    db.session.delete(student)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def updateStudent(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(student)
        db.session.commit()
        if student:
            student.name = request.form['name']
            student.email = request.form['email']
            student.contact = request.form['contact']
            student.course = request.form['course']

            update_student= Student(name=student.name, email=student.email, contact=student.contact, course=student.course) # Create a new instance of StudentModel with updated data
            db.session.update(update_student)  # Add the updated student to the session
            db.session.commit()
            return redirect('/')
    return render_template('update.html', student=student)


if __name__ == '__main__':
    with app.app_context():
        # Create the database tables
        db.create_all()
        app.run(debug=True)