import sqlite3

def connect_db():
    return sqlite3.connect('database.db')

def save_review(book_id, user_name, rating, comment):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reviews (book_id, user_name, rating, comment) VALUES (?, ?, ?, ?)',
                   (book_id, user_name, rating, comment))
    conn.commit()
    conn.close()

def get_reviews(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT user_name, rating, comment FROM reviews WHERE book_id = ?', (book_id,))
    reviews = cursor.fetchall()
    conn.close()
    return reviews
