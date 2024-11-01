import sqlite3
import random
import string
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# Set up the database
def init_db():
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS urls (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        short TEXT NOT NULL,
                        original TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

# Helper function to generate random short URLs
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Endpoint to shorten a URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json.get('url')
    if not original_url:
        return jsonify({'error': 'Missing URL'}), 400

    short_url = generate_short_url()
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO urls (short, original) VALUES (?, ?)', (short_url, original_url))
    conn.commit()
    conn.close()

    return jsonify({'short_url': request.host_url + short_url})

# Endpoint to redirect to the original URL
@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT original FROM urls WHERE short = ?', (short_url,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return redirect(row[0])
    else:
        return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
