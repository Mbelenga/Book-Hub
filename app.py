from flask import Flask, render_template, request, redirect, url_for

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
    # This is a placeholder for your search function
    query = request.json.get('query')
    books = [
        {
            "title": "Sample Book",
            "authors": ["Author Name"],
            "thumbnail": "/static/images/sample.jpg",
            "description": "Sample description of the book."
        },
        # Add more book entries here
    ]
    return jsonify(books=books)

if __name__ == '__main__':
    app.run(debug=True)
