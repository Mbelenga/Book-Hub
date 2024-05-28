import requests

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
OPEN_LIBRARY_SEARCH_URL = "http://openlibrary.org/search.json"
GUTENBERG_API_URL = "http://gutendex.com/books"

def search_books(query):
    response = requests.get(GOOGLE_BOOKS_API_URL, params={'q': query})
    return response.json().get('items', [])

def search_books_by_category(category):
    # Implement category search logic if available for Google Books, Open Library, or Project Gutenberg
    response = requests.get(OPEN_LIBRARY_SEARCH_URL, params={'subject': category})
    return response.json().get('docs', [])

def get_new_releases():
    # Implement new releases fetch logic if available from any source
    response = requests.get(GOOGLE_BOOKS_API_URL, params={'orderBy': 'newest'})
    return response.json().get('items', [])

def get_book_details(book_id):
    response = requests.get(f"{GOOGLE_BOOKS_API_URL}/{book_id}")
    return response.json()

def get_books_from_gutenberg():
    response = requests.get(GUTENBERG_API_URL)
    return response.json().get('results', [])

def download_book_from_gutenberg(book_id):
    response = requests.get(f"{GUTENBERG_API_URL}/{book_id}")
    return response.json()
