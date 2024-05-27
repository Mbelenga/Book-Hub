from flask import Flask, render_template, request, redirect, url_for, jsonify
from book_search import search_books

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('user.html')

@app.route('/categories')
def categories():
    return render_template('categories.html')

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
    books_data = search_books(query)
    books = []
    for book in books_data:
        volume_info = book['volumeInfo']
        books.append({
            "title": volume_info.get('title', 'No title available'),
            "authors": volume_info.get('authors', ['No authors available']),
            "thumbnail": volume_info.get('imageLinks', {}).get('thumbnail', ''),
            "description": volume_info.get('description', 'No description available')
        })
    return jsonify(books=books)

if __name__ == '__main__':
    app.run(debug=True)
