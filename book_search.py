import requests
import os

GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'
OPEN_LIBRARY_API_URL = 'http://openlibrary.org/search.json'
GUTENBERG_API_URL = 'https://gutenberg.org/ebooks/'

def search_books(query):
    google_books = search_google_books(query)
    open_library_books = search_open_library(query)
    gutenberg_books = search_gutenberg_books(query)
    return google_books + open_library_books + gutenberg_books

def search_google_books(query):
    params = {'q': query, 'key': os.getenv('GOOGLE_API_KEY')}
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        books = [
            {
                "id": book['id'],
                "title": book['volumeInfo'].get('title', 'No title available'),
                "authors": book['volumeInfo'].get('authors', ['No authors available']),
                "thumbnail": book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                "description": book['volumeInfo'].get('description', 'No description available'),
                "previewLink": book['volumeInfo'].get('previewLink', '')
            }
            for book in data.get('items', [])
        ]
        return books
    return []

def search_open_library(query):
    response = requests.get(OPEN_LIBRARY_API_URL, params={'q': query})
    if response.status_code == 200:
        data = response.json()
        books = [
            {
                "id": book['key'].split('/')[-1],
                "title": book.get('title', 'No title available'),
                "authors": [author['name'] for author in book.get('author_name', [])],
                "thumbnail": '',
                "description": book.get('first_sentence', 'No description available'),
                "previewLink": f"https://openlibrary.org{book['key']}"
            }
            for book in data.get('docs', [])
        ]
        return books
    return []

def search_gutenberg_books(query):
    response = requests.get(GUTENBERG_API_URL, params={'query': query})
    if response.status_code == 200:
        data = response.json()
        books = [
            {
                "id": book['id'],
                "title": book.get('title', 'No title available'),
                "authors": [author['name'] for author in book.get('authors', [])],
                "thumbnail": '',
                "description": book.get('download_count', 'No description available'),
                "previewLink": f"https://gutenberg.org/ebooks/{book['id']}"
            }
            for book in data.get('results', [])
        ]
        return books
    return []

def get_book_details(book_id):
    # Implement fetching book details from the appropriate source
    pass

def get_new_releases():
    # Implement fetching new releases
    pass
