from flask import Flask, render_template, request, redirect, url_for, jsonify
from book_search import search_books, search_books_by_category, get_book_details, get_new_releases
from database import save_review, get_reviews

app = Flask(__name__)

@app.route('/')
def home():
    new_releases = get_new_releases()
    return render_template('user.html', new_releases=new_releases)

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
    reviews = get_reviews(book_id)
    return render_template('book.html', book=book_details, reviews=reviews)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        book_id = request.form['book_id']
        book_title = request.form['book_title']
        rating = request.form['rating']
        review = request.form['review']
        save_review(book_id, book_title, rating, review)
        return redirect(url_for('book', book_id=book_id))
    return render_template('reviews.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    books = search_books(query)
    return jsonify(books=books)

if __name__ == '__main__':
    app.run(debug=True)
