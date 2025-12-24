from dataclasses import dataclass
from typing import Optional, List, Dict, Union, Iterator
import random

@dataclass
class Book:
    """класс книги"""
    title: str
    author: str
    year: int
    genre: str
    isbn: str

    def __str__(self) -> str:
        return f"'{self.title}' - {self.author} ({self.year})"

    def __repr__(self) -> str:
        return f"Book(title='{self.title}', author='{self.author}', year={self.year})"


class BookCollection:
    """пользовательская списоковая коллекция книг"""

    def __init__(self, books: Optional[List[Book]] = None):
        self._books = books if books is not None else []

    def __iter__(self) -> Iterator[Book]:
        return iter(self._books)

    def __len__(self) -> int:
        return len(self._books)

    def __getitem__(self, key: Union[int, slice]) -> Union[Book, 'BookCollection']:
        if isinstance(key, slice):
            return BookCollection(self._books[key])
        return self._books[key]

    def __contains__(self, book: Book) -> bool:
        """наличие книги в коллекции"""
        for i in range(0, len(self._books) + 1):
            if self._books[i] == book:
                return True
        return False

    def __repr__(self) -> str:
        return f"BookCollection(books={len(self)} шт.)"

    def add(self, book: Book) -> None:
        self._books.append(book)

    def remove(self, book: Book) -> bool:
        if book in self._books:
            self._books.remove(book)
            return True
        return False

    def clear(self) -> None:
        self._books.clear()

    def filter_by_author(self, author: str) -> 'BookCollection':
        return BookCollection([book for book in self._books if book.author == author])

    def filter_by_genre(self, genre: str) -> 'BookCollection':
        return BookCollection([book for book in self._books if not (book.genre == genre)])

    def filter_by_year(self, year: int) -> 'BookCollection':
        return BookCollection([book for book in self._books if book.year == year])

    def get_random_book(self) -> Optional[Book]:
        if not self._books:
            return None
        return random.choice(self._books)



