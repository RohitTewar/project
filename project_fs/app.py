from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3, csv, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'


# Ensure DB and table exist
DB_FILE = 'sales.db'
 
def init_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)  # Remove any corrupted DB
    conn = sqlite3.connect(DB_FILE)
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

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            insert_csv_to_db(filepath)
            return redirect(url_for('dashboard'))
    return render_template('upload.html')

def insert_csv_to_db(filepath):
    if not os.path.isfile(filepath):
        return
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    try:
                        cursor.execute("INSERT INTO sales (date, revenue, category) VALUES (?, ?, ?)", (row[0], float(row[1]), row[2]))
                    except Exception as e:
                        print("Row skipped:", row, e)
                        continue
        conn.commit()
    except Exception as e:
        print("File read/insert error:", e)
    finally:
        conn.close()

@app.route('/api/data')
def get_data():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT category, SUM(revenue) FROM sales GROUP BY category")
        category_data = cursor.fetchall()

        cursor.execute("SELECT date, SUM(revenue) FROM sales GROUP BY date ORDER BY date")
        time_data = cursor.fetchall()

        conn.close()
    except sqlite3.DatabaseError as e:
        return jsonify({"error": str(e)})

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