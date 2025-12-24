from src.Library.book import BookCollection, Book
from typing import Optional, Dict
from src.Library.index import IndexDict


class BaseLibrary:
    """базовая библиотека"""

    def __init__(self, name: str):
        self.name = name
        self._books = BookCollection()

    def __len__(self) -> int:
        return len(self._books)

    def __contains__(self, book: Book) -> bool:
        return book in self._books

    def add_book(self, book: Book) -> None:
        """Добавление книги в библиотеку"""
        self._books.add(book)

    def remove_book(self, book: Book) -> bool:
        """Удаление книги из библиотеки"""
        return self._books.remove(book)

    def get_book_count(self) -> int:
        """Получение количества книг"""
        return len(self._books)


class Library(BaseLibrary):
    def __init__(self, name: str):
        super().__init__(name)
        self._index = IndexDict()
        self._borrowed_books: Dict[str, str] = {}

    def __add__(self, book: Book) -> 'Library':
        """library + book"""
        self.add_book(book)
        return self

    def __call__(self, query: str) -> BookCollection:
        """library('автор')"""
        return self.search_books(query)

    def __repr__(self) -> str:
        return f"Library(name='{self.name}', books={len(self)}, borrowed={len(self._borrowed_books)})"

    def add_book(self, book: Book) -> None:
        """Переопределение метода"""
        super().add_book(book)
        self._index.add_book(book)

    def remove_book(self, isbn: str) -> bool:
        """Удаление книги по ISBN"""
        book = self._index.search_by_isbn(isbn)
        if book and book in self._books:
            self._books.remove(book)
            self._index.remove_book(isbn)
            if isbn in self._borrowed_books:
                del self._borrowed_books[isbn]
            return True
        return False

    def search_books(self, query: str) -> BookCollection:
        """Поиск книг"""
        result = BookCollection()

        # поиск по автору
        books_by_author = self._index.search_by_author(query)
        if books_by_author:
            result = BookCollection(books_by_author)
        else:
            # по году
            if query.isdigit():
                year_str = query.strip()
                year = int(year_str)
                if year < 100:
                    year += 1900
                books_by_year = self._index.search_by_year(year)
                if books_by_year:
                    result = BookCollection(books_by_year)
            # по жанру
            else:
                result = self._books.filter_by_genre(query)

        return result

    def borrow_book(self, reader: str, isbn: str) -> bool:
        """Выдача книги читателю"""
        if isbn not in self._index:
            return False

        if isbn in self._borrowed_books:
            return False  # уже выдана

        self._borrowed_books[isbn] = reader
        return True

    def return_book(self, isbn: str) -> bool:
        """Возврат книги читателем"""
        if isbn not in self._borrowed_books:
            return False

        del self._borrowed_books[isbn]
        return True

    def update_index(self) -> None:
        """Обновление индексов"""
        self._index.clear()
        for book in self._books:
            self._index.add_book(book)

    def get_random_book(self) -> Optional[Book]:
        """Получение случайной книги"""
        return self._books.get_random_book()


class DigitalLibrary(Library):
    """цифровая библиотека"""

    def __init__(self, name: str, max_digital_copies: int = 1000):
        super().__init__(name)
        self.max_digital_copies = max_digital_copies
        self._digital_copies: Dict[str, int] = {}  # ISBN -> количество копий

    def __repr__(self) -> str:
        return f"DigitalLibrary(name='{self.name}', books={len(self)}, digital_titles={len(self._digital_copies)})"

    def add_digital_copy(self, book: Book, copies: int = 1) -> None:
        """Добавление цифровой копии книги"""
        super().add_book(book)
        if book.isbn not in self._digital_copies:
            self._digital_copies[book.isbn] = 0
        self._digital_copies[book.isbn] = min(
            self._digital_copies[book.isbn] + copies,
            self.max_digital_copies
        )

    def borrow_book(self, isbn: str, reader: str) -> bool:
        """Переопределение выдачи книги"""
        if isbn not in self._digital_copies or self._digital_copies[isbn] <= 0:
            return False

        self._digital_copies[isbn] -= 1
        return True

    def return_book(self, isbn: str) -> bool:
        """Возврат книги в цифровую библиотеку"""
        if isbn not in self._digital_copies:
            return False

        self._digital_copies[isbn] += 1
        return True

