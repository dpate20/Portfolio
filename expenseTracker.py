import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# Set up the database
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        date TEXT NOT NULL,
                        notes TEXT,
                        payment_method TEXT
                      )''')
    conn.commit()
    conn.close()

# Endpoint to add an expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    title = data.get('title')
    amount = data.get('amount')
    category = data.get('category')
    date = data.get('date', datetime.now().strftime("%Y-%m-%d"))
    notes = data.get('notes', '')
    payment_method = data.get('payment_method', 'cash')

    if not title or not amount or not category:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (title, amount, category, date, notes, payment_method) VALUES (?, ?, ?, ?, ?, ?)',
                   (title, amount, category, date, notes, payment_method))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Expense added successfully!'}), 201

# Endpoint to get all expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    rows = cursor.fetchall()
    conn.close()

    expenses = []
    for row in rows:
        expenses.append({
            'id': row[0],
            'title': row[1],
            'amount': row[2],
            'category': row[3],
            'date': row[4],
            'notes': row[5],
            'payment_method': row[6]
        })

    return jsonify(expenses)

# Endpoint to get expenses by category
@app.route('/expenses/category/<category>', methods=['GET'])
def get_expenses_by_category(category):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses WHERE category = ?', (category,))
    rows = cursor.fetchall()
    conn.close()

    expenses = []
    for row in rows:
        expenses.append({
            'id': row[0],
            'title': row[1],
            'amount': row[2],
            'category': row[3],
            'date': row[4],
            'notes': row[5],
            'payment_method': row[6]
        })

    return jsonify(expenses)

# Endpoint to get expenses by date range
@app.route('/expenses/date_range', methods=['GET'])
def get_expenses_by_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({'error': 'Missing required date range fields'}), 400

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses WHERE date BETWEEN ? AND ?', (start_date, end_date))
    rows = cursor.fetchall()
    conn.close()

    expenses = []
    for row in rows:
        expenses.append({
            'id': row[0],
            'title': row[1],
            'amount': row[2],
            'category': row[3],
            'date': row[4],
            'notes': row[5],
            'payment_method': row[6]
        })

    return jsonify(expenses)

# Endpoint to delete an expense by ID
@app.route('/delete_expense/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Expense deleted successfully!'}), 200

# Endpoint to get a random motivational message
@app.route('/motivational_message', methods=['GET'])
def get_motivational_message():
    messages = [
        "Keep going! You're doing great!",
        "Every penny saved is a penny earned!",
        "Budgeting is the first step to financial freedom!",
        "Stay on track, your future self will thank you!",
        "Small steps lead to big changes!"
    ]
    return jsonify({'message': random.choice(messages)})

# Endpoint to get total expenses summary
@app.route('/expenses/summary', methods=['GET'])
def get_expenses_summary():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    rows = cursor.fetchall()
    conn.close()

    summary = []
    for row in rows:
        summary.append({
            'category': row[0],
            'total_amount': row[1]
        })

    return jsonify(summary)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
