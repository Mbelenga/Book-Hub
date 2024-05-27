import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'
OPEN_LIBRARY_API_URL = 'https://openlibrary.org/api/books'
PROJECT_GUTENBERG_URL = 'http://gutenberg.org/ebooks/'

API_KEY = os.getenv('API_KEY')

def search_books(query):
    params = {
        'q': query,
        'key': API_KEY
    }
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        books = data.get('items', [])
        return format_books(books)
    else:
        print(f'Error: {response.status_code}')
        return []

def search_books_by_category(category):
    query = f'subject:{category}'
    return search_books(query)

def get_new_releases():
    # Implement fetching new releases (this can be an API call to Google Books, Open Library, etc.)
    return []

def get_book_details(book_id):
    url = f'{GOOGLE_BOOKS_API_URL}/{book_id}'
    response = requests.get(url, params={'key': API_KEY})
    if response.status_code == 200:
        data = response.json()
        return format_book(data)
    else:
        print(f'Error: {response.status_code}')
        return None

def format_books(items):
    books = []
    for item in items:
        book = format_book(item)
        books.append(book)
    return books

def format_book(item):
    volume_info = item.get('volumeInfo', {})
    return {
        'id': item.get('id'),
        'title': volume_info.get('title'),
        'authors': volume_info.get('authors', []),
        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail'),
        'description': volume_info.get('description', ''),
        'previewLink': volume_info.get('previewLink')
    }

def get_books_from_gutenberg():
    # Implement the logic to fetch books from Project Gutenberg
    return []

def download_book_from_gutenberg(book_id):
    # Implement the logic to download the book content from Project Gutenberg
    return ""
