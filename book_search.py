import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv('API_KEY')
GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'
OPEN_LIBRARY_SEARCH_URL = 'http://openlibrary.org/search.json'
OPEN_LIBRARY_BOOK_URL = 'https://openlibrary.org/api/books'

def search_books(query):
    params = {
        'q': query,
        'key': API_KEY
    }
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        books = data.get('items', [])
        return books
    else:
        print(f'Error: {response.status_code}')
        return []

def search_books_by_category(category):
    query = f'subject:{category}'
    return search_books(query)

def get_books_from_gutenberg():
    # For simplicity, we'll use a static list of books from Project Gutenberg
    books = [
        {'id': '84', 'title': 'Frankenstein', 'author': 'Mary Shelley'},
        {'id': '1342', 'title': 'Pride and Prejudice', 'author': 'Jane Austen'},
        {'id': '11', 'title': 'Alice\'s Adventures in Wonderland', 'author': 'Lewis Carroll'}
    ]
    return books

def download_book_from_gutenberg(book_id):
    book_url = f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt'
    response = requests.get(book_url)
    if response.status_code == 200:
        return response.text
    else:
        return "Error: Could not retrieve the book content."

def search_open_library(query):
    params = {
        'q': query
    }
    response = requests.get(OPEN_LIBRARY_SEARCH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        books = data.get('docs', [])
        return books
    else:
        print(f'Error: {response.status_code}')
        return []

def get_open_library_book(book_id):
    params = {
        'bibkeys': f'OLID:{book_id}',
        'format': 'json',
        'jscmd': 'data'
    }
    response = requests.get(OPEN_LIBRARY_BOOK_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        book_key = f'OLID:{book_id}'
        if book_key in data:
            return data[book_key]
    return None
