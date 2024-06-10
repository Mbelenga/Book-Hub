from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
import sqlite3

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from book_search import search_books, search_books_by_category

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configurations for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///init.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create the database and the table(s)
with app.app_context():
    db.create_all()

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_content = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/modern')
def modern():
    return render_template('modern.html')

@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route('/category/<category_name>')
def category(category_name):
    books = search_books_by_category(category_name)
    formatted_books = [
        {
            "title": book['volumeInfo'].get('title', 'No title available'),
            "authors": book['volumeInfo'].get('authors', ['No authors available']),
            "thumbnail": book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
            "description": book['volumeInfo'].get('description', 'No description available'),
            "previewLink": book['volumeInfo'].get('previewLink', '')
        }
        for book in books
    ]
    return render_template('category_books.html', books=formatted_books, category=category_name)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    return render_template('reviews.html')

@app.route('/my_reviews')
def my_reviews():
    return render_template('my_reviews.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    books = search_books(query)
    formatted_books = [
        {
            "title": book['volumeInfo'].get('title', 'No title available'),
            "authors": book['volumeInfo'].get('authors', ['No authors available']),
            "thumbnail": book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
            "description": book['volumeInfo'].get('description', 'No description available')
        }
        for book in books
    ]
    return jsonify(books=formatted_books)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            return 'Username already exists. Please choose another.'
        
        users[username] = {'password': generate_password_hash(password)}
        session['username'] = username
        return redirect(url_for('user_page'))
    
    return render_template('signup.html')

@app.route('/user')
def user_page():
    if 'username' in session:
        return render_template('user.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('user_page'))
        else:
            return 'Invalid credentials. Please try again.'
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Successfully logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
