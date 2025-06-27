from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3, csv, os
from werkzeug.utils import secure_filename

# Flask web application to handle user authentication, file upload, and data visualization
app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ensure DB and table exist
def init_db():
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        revenue REAL,
        category TEXT
    )''')
    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Replace with DB or more secure auth
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            insert_csv_to_db(filepath)
            flash('File uploaded and data inserted')
            return redirect(url_for('dashboard'))
    return render_template('upload.html')

def insert_csv_to_db(filepath):
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) >= 3:
                cursor.execute("INSERT INTO sales (date, revenue, category) VALUES (?, ?, ?)", row)
    conn.commit()
    conn.close()

@app.route('/api/data')
def get_data():
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(revenue) FROM sales GROUP BY category")
    category_data = cursor.fetchall()

    cursor.execute("SELECT date, revenue FROM sales ORDER BY date")
    time_data = cursor.fetchall()
    conn.close()

    pie_labels = [row[0] for row in category_data]
    pie_values = [row[1] for row in category_data]

    line_labels = [row[0] for row in time_data]
    line_values = [row[1] for row in time_data]

    return jsonify({
        "pie": {"labels": pie_labels, "values": pie_values},
        "line": {"labels": line_labels, "values": line_values}
    })

if __name__ == '__main__':
    app.run(debug=True)
