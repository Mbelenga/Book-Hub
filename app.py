from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('user.html')

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
