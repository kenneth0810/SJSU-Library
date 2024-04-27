import requests, json, random

url = 'https://openlibrary.org/trending/yearly.json'

# request json data from OpenLibrary to fetch top ~100 trending books of the year
def get_trending_books():
    with open('data/trending_books.json', 'w') as datafile:
        data = requests.get(url).json()['works']
        books = []
        for book, i in zip(data, range(1, len(data))):
            # use this object format to create a fixture for populating the Book database
            book_obj = {
                'model': 'sjsu_library.book',
                'pk': i,
                'fields': {
                    'title': book['title'],
                    'author': book['author_name'][0],
                    'year': book['first_publish_year'],
                    'link': f'https://openlibrary.org{book["key"]}',
                    'count': random.randint(1,5)
                }
            }
            books.append(book_obj)

        json.dump(books, datafile, indent=4)

if __name__ == '__main__':
    get_trending_books()