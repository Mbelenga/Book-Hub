from flask import Flask, render_template, request, redirect, url_for, jsonify
from book_search import search_books, search_books_by_category, get_book_details, get_new_releases
from database import save_review, get_reviews

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('user.html')

@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route('/category/<category_name>')
def category(category_name):
    books = search_books_by_category(category_name)
    return render_template('category_books.html', books=books, category=category_name)

@app.route('/book/<book_id>')
def book(book_id):
    book_details = get_book_details(book_id)
    return render_template('book.html', book=book_details)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        book_title = request.form['book-title']
        rating = request.form['rating']
        review = request.form['review']
        # Save the review to the database
        save_review(book_title, rating, review)
        return redirect(url_for('reviews'))
    reviews = get_reviews()
    return render_template('reviews.html', reviews=reviews)

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    books = search_books(query)
    formatted_books = [
        {
            "id": book['id'],
            "title": book['volumeInfo'].get('title', 'No title available'),
            "authors": book['volumeInfo'].get('authors', ['No authors available']),
            "thumbnail": book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
            "description": book['volumeInfo'].get('description', 'No description available'),
            "previewLink": book['volumeInfo'].get('previewLink', '')
        }
        for book in books
    ]
    return jsonify(books=formatted_books)

@app.route('/new-releases')
def new_releases():
    releases = get_new_releases()
    return render_template('new_releases.html', releases=releases)

if __name__ == '__main__':
    app.run(debug=True)
