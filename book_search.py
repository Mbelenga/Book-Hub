import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Print out API_KEY to verify it's loaded correctly
print(API_KEY)

API_KEY = os.getenv('API_KEY')
GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'

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
