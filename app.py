from flask import Flask, render_template, request, redirect, url_for, jsonify
from book_search import search_books, search_books_by_category, get_books_from_gutenberg, download_book_from_gutenberg, get_new_releases, get_book_details

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
            "id": book['key'].split('/')[-1],
            "title": book['title'],
            "author": book.get('author_name', ['Unknown'])[0]
        }
        for book in books
    ]
    return render_template('category_books.html', books=formatted_books, category=category_name)

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
        # Process the form data here (e.g., save it to a database)
        return redirect(url_for('reviews'))
    return render_template('reviews.html')

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
