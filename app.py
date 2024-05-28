from flask import Flask, render_template, request, redirect, url_for, jsonify
from book_search import search_books, search_books_by_category

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
    formatted_books = [
        {
            "title": book['volumeInfo'].get('title', 'No title available'),
            "authors": book['volumeInfo'].get('authors', ['No authors available']),
            "thumbnail": book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
            "description": book['volumeInfo'].get('description', 'No description available')
        }
        for book in books
    ]
    return render_template('category_books.html', books=formatted_books, category=category_name)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        book_title = request.form['book-title']
        rating = request.form['rating']
        review = request.form['review']
        # Process the form data here (e.g., save it to a database)
        return redirect(url_for('reviews'))
    return render_template('reviews.html')

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

if __name__ == '__main__':
    app.run(debug=True)
