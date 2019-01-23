class singlebook:
    def __init__(self, book, keyword):
        self.book = book
        self.keyword = keyword

    def get(self):
        book = {
            'keyword': self.keyword,
            'isbn': self.keyword,
            'title': self.book['title'],
            'publisher': self.book['publisher'],
            'pages': self.book['pages'] or '',
            'author': self.book['author'],
            'price': self.book['price'],
            'summary': self.book['summary'] or '',
            'image': self.book['image'],
            'total': 1,
            'intro': self.intro
        }
        return book

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.book['author'], self.book['publisher'], self.book['price']])
        intros = map(lambda x: str(x), intros)
        return '/'.join(intros)


class BookCollection:
    def __init__(self, data, keyword):
        self.data = data
        self.keyword = keyword
        self.books = []

    def getBook(self):
        self.books = [singlebook(book).get() for book in self.data]
        book = {
            'books': self.books
        }
        return book
