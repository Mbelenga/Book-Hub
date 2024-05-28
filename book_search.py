import requests

# Google Books API key (replace with your actual API key)
GOOGLE_BOOKS_API_KEY = 'YOUR_GOOGLE_BOOKS_API_KEY'

# Function to search books from Google Books API
def search_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []

# Function to get new releases from Google Books API
def get_new_releases():
    url = f"https://www.googleapis.com/books/v1/volumes?q=new+releases&orderBy=newest&key={GOOGLE_BOOKS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []

# Function to get book details from Google Books API
def get_book_details(book_id):
    url = f"https://www.googleapis.com/books/v1/volumes/{book_id}?key={GOOGLE_BOOKS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# Function to search books by category from Open Library
def search_books_by_category(category_name):
    url = f"http://openlibrary.org/subjects/{category_name}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['works']
    return []

# Function to get books from Project Gutenberg
def get_books_from_gutenberg(category=None):
    # Project Gutenberg API does not support categories directly,
    # so this is a placeholder for actual implementation.
    url = "http://gutendex.com/books"
    if category:
        url += f"?topic={category}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

# Function to download book content from Project Gutenberg
def download_book_from_gutenberg(book_id):
    url = f"http://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return "Book content could not be retrieved."

def search_books_by_category(category):
    query = f'subject:{category}'
    return search_books(query)
