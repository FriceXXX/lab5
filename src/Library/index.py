from src.Library.book import Book
from typing import Optional, List, Dict, Union, Iterator

class IndexDict:
    """пользовательская словарная коллекция для индексации книг"""

    def __init__(self):
        self._isbn_index: Dict[str, Book] = {}
        self._author_index: Dict[str, List[Book]] = {}
        self._year_index: Dict[int, List[Book]] = {}

    def __len__(self) -> int:
        return len(self._isbn_index)

    def __getitem__(self, key: str) -> Union[Book, List[Book]]:
        """Доступ по ключу (ISBN, автор, год)"""
        if key in self._isbn_index:
            return self._isbn_index[key]
        elif key in self._author_index:
            return self._author_index[key]
        elif str(key).isdigit() and int(key) in self._year_index:
            return self._year_index[int(key)]
        raise KeyError(f"Ключ '{key}' не найден в индексах")

    def __iter__(self) -> Iterator[str]:
        """Итерация по ISBN"""
        return iter(self._isbn_index)

    def __contains__(self, isbn: str) -> bool:
        """наличия ISBN в индексе"""
        return isbn in self._isbn_index

    def __repr__(self) -> str:
        return f"IndexDict(книг: {len(self._isbn_index)}, авторов: {len(self._author_index)}, годов: {len(self._year_index)})"

    def add_book(self, book: Book) -> None:
        """Добавление книги во все индексы"""
        # Индекс по ISBN
        self._isbn_index[book.isbn] = book

        # по автору
        if book.author not in self._author_index:
            self._author_index[book.author] = []
        self._author_index[book.author].append(book)

        # по году
        if book.year not in self._year_index:
            self._year_index[book.year] = []
        self._year_index[book.year].append(book)

    def remove_book(self, isbn: str) -> bool:
        """Удаление книги из всех индексов"""
        if isbn not in self._isbn_index:
            return False

        book = self._isbn_index[isbn]

        # по ISBN
        del self._isbn_index[isbn]

        # по автору
        if book.author in self._author_index:
            self._author_index[book.author].remove(book)
            if not self._author_index[book.author]:
                del self._author_index[book.author]

        # по году
        if book.year in self._year_index:
            self._year_index[book.year].remove(book)
            if not self._year_index[book.year]:
                del self._year_index[book.year]

        return True

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        return self._isbn_index.get(isbn)

    def search_by_author(self, author: str) -> List[Book]:
        return self._author_index.get(author, [])

    def search_by_year(self, year: int) -> List[Book]:
        return self._year_index.get(year, [])

    def clear(self) -> None:
        self._isbn_index.clear()
        self._author_index.clear()
        self._year_index.clear()
