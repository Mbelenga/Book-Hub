from flask import Flask, render_template, request, redirect, url_for, jsonify
from book_search import search_books, search_books_by_category, get_books_from_gutenberg, download_book_from_gutenberg, get_new_releases, get_book_details
from database import save_review, get_reviews

app = Flask(__name__)

@app.route('/')
def home():
    new_releases = get_new_releases()
    formatted_books = [
        {
            "id": book['id'],
            "title": book['volumeInfo'].get('title', 'No title available'),
            "authors": book['volumeInfo'].get('authors', ['No authors available']),
            "thumbnail": book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
            "description": book['volumeInfo'].get('description', 'No description available'),
            "previewLink": book['volumeInfo'].get('previewLink', '')
        }
        for book in new_releases
    ]
    return render_template('user.html', new_releases=formatted_books)

@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route('/category/<category_name>')
def category(category_name):
    books = search_books_by_category(category_name)
    formatted_books = [
        {
            "id": book.get('cover_edition_key', book['key']),
            "title": book.get('title', 'No title available'),
            "authors": [author['name'] for author in book.get('authors', [{'name': 'No author available'}])],
            "thumbnail": f"http://covers.openlibrary.org/b/ID/{book.get('cover_id', 'no-cover')}-L.jpg",
            "description": book.get('description', 'No description available') if isinstance(book.get('description'), str) else book.get('description', {}).get('value', 'No description available'),
            "previewLink": f"https://openlibrary.org{book.get('key')}"
        }
        for book in books
    ]
    return render_template('category_books.html', books=formatted_books, category=category_name)

@app.route('/book/<book_id>')
def book(book_id):
    book_content = download_book_from_gutenberg(book_id)
    return render_template('book.html', content=book_content)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        book_title = request.form['book-title']
        rating = request.form['rating']
        review = request.form['review']
        # Process the form data here (e.g., save it to a database)
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

if __name__ == '__main__':
    app.run(debug=True)
