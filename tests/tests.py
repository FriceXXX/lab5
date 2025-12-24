import pytest
from src.Library.index import IndexDict
from src.Library.book import Book, BookCollection
from src.Library.library import Library, DigitalLibrary

def test_book_creation():
    book = Book("Test Book", "Test Author", 2023, "Test Genre", "123-456-789")

    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.year == 2023
    assert book.genre == "Test Genre"
    assert book.isbn == "123-456-789"

def test_book_collection_basic():
    book1 = Book("Book 1", "Author 1", 2021, "Genre 1", "111")
    book2 = Book("Book 2", "Author 2", 2022, "Genre 2", "222")

    collection = BookCollection([book1, book2])

    assert len(collection) == 2
    assert book1 in collection
    assert book2 in collection


def test_book_collection_add_remove():
    collection = BookCollection()
    book = Book("Test Book", "Test Author", 2023, "Test", "123")

    # Добавление
    collection.add(book)
    assert len(collection) == 1
    assert book in collection

    # Удаление
    result = collection.remove(book)
    assert result is True
    assert len(collection) == 0
    assert book not in collection

    # Удаление несуществующей книги
    result = collection.remove(book)
    assert result is False


def test_book_collection_iteration():
    books = [
        Book("Book 1", "Author 1", 2021, "Genre 1", "111"),
        Book("Book 2", "Author 2", 2022, "Genre 2", "222"),
        Book("Book 3", "Author 3", 2023, "Genre 3", "333")
    ]

    collection = BookCollection(books)

    # проверка итерации
    titles = [book.title for book in collection]
    assert titles == ["Book 1", "Book 2", "Book 3"]

    # проверка индексации
    assert collection[0] == books[0]
    assert collection[-1] == books[-1]

    # проверка срезов
    slice_result = collection[1:3]
    assert len(slice_result) == 2
    assert slice_result[0] == books[1]


def test_book_collection_filter():
    book1 = Book("Book 1", "Author A", 2021, "Fiction", "111")
    book2 = Book("Book 2", "Author A", 2022, "Non-Fiction", "222")
    book3 = Book("Book 3", "Author B", 2021, "Fiction", "333")

    collection = BookCollection([book1, book2, book3])

    # фильтрация по автору
    author_filtered = collection.filter_by_author("Author A")
    assert len(author_filtered) == 2
    assert all(book.author == "Author A" for book in author_filtered)

    # фильтрация по жанру
    genre_filtered = collection.filter_by_genre("Fiction")
    assert len(genre_filtered) == 2
    assert all(book.genre == "Fiction" for book in genre_filtered)

    # фильтрация по году
    year_filtered = collection.filter_by_year(2021)
    assert len(year_filtered) == 2
    assert all(book.year == 2021 for book in year_filtered)


def test_index_dict_basic():
    index = IndexDict()
    book = Book("Test Book", "Test Author", 2023, "Test", "123")

    # Добавление книги
    index.add_book(book)
    assert len(index) == 1
    assert "123" in index

    # Поиск по ISBN
    found_book = index.search_by_isbn("123")
    assert found_book == book
    assert index["123"] == book

    # Поиск по автору
    author_books = index.search_by_author("Test Author")
    assert len(author_books) == 1
    assert author_books[0] == book
    assert index["Test Author"] == author_books

    # Поиск по году
    year_books = index.search_by_year(2023)
    assert len(year_books) == 1
    assert year_books[0] == book
    assert index[2023] == year_books


def test_index_dict_remove():
    book1 = Book("Book 1", "Author A", 2021, "Fiction", "111")
    book2 = Book("Book 2", "Author A", 2022, "Non-Fiction", "222")

    index = IndexDict()
    index.add_book(book1)
    index.add_book(book2)

    assert len(index) == 2
    assert len(index.search_by_author("Author A")) == 2

    # Удаление одной книги
    result = index.remove_book("111")
    assert result is True
    assert len(index) == 1
    assert len(index.search_by_author("Author A")) == 1

    # Удаление несуществующей книги
    result = index.remove_book("999")
    assert result is False


def test_index_dict_iteration():
    books = [
        Book("Book 1", "Author 1", 2021, "Genre 1", "111"),
        Book("Book 2", "Author 2", 2022, "Genre 2", "222"),
    ]

    index = IndexDict()
    for book in books:
        index.add_book(book)

    # Проверка итерации по ISBN
    isbns = list(index)
    assert "111" in isbns
    assert "222" in isbns
    assert len(isbns) == 2

def test_library_creation():
    library = Library("Test Library")

    assert library.name == "Test Library"
    assert len(library) == 0
    assert "Library" in repr(library)


def test_library_add_remove_books():
    library = Library("Test Library")
    book = Book("Test Book", "Test Author", 2023, "Test", "123")

    # Добавление книги
    library.add_book(book)
    assert len(library) == 1
    assert book in library

    # Проверка  __add__
    book2 = Book("Book 2", "Author 2", 2024, "Genre", "456")
    library = library + book2
    assert len(library) == 2

    # Удаление книги по ISBN
    result = library.remove_book("123")
    assert result is True
    assert len(library) == 1

    # Удаление несуществующей книги
    result = library.remove_book("999")
    assert result is False


def test_library_search():
    library = Library("Test Library")

    books = [
        Book("Book 1", "Author A", 2021, "Fiction", "111"),
        Book("Book 2", "Author A", 2022, "Non-Fiction", "222"),
        Book("Book 3", "Author B", 2021, "Fiction", "333"),
    ]

    for book in books:
        library.add_book(book)

    # Поиск по жанру
    results = library.search_books("Fiction")
    assert len(results) == 2
    assert all(book.genre == "Fiction" for book in results)

    # Поиск по году
    results = library.search_books("2021")
    assert len(results) == 2
    assert all(book.year == 2021 for book in results)

    # Поиск несуществующего
    results = library.search_books("NonExistent")
    assert len(results) == 0


def test_library_borrow_return():
    library = Library("Test Library")
    book = Book("Test Book", "Test Author", 2023, "Test", "123")
    library.add_book(book)

    # Выдача
    result = library.borrow_book("123", "Reader 1")
    assert result is True

    # Книга уже выдана
    result = library.borrow_book("123", "Reader 2")
    assert result is False

    # Возврат
    result = library.return_book("123")
    assert result is True

    # Выдача после возврата
    result = library.borrow_book("123", "Reader 2")
    assert result is True

    # Возврат невыданной книги
    result = library.return_book("999")
    assert result is False


def test_library_update_index():
    library = Library("Test Library")

    books = [
        Book("Book 1", "Author A", 2021, "Fiction", "111"),
        Book("Book 2", "Author B", 2022, "Non-Fiction", "222"),
    ]

    for book in books:
        library.add_book(book)

    assert len(library._index) == 2

    library._index.clear()
    assert len(library._index) == 0

    library.update_index()
    assert len(library._index) == 2

    results = library.search_books("Author A")
    assert len(results) == 1

def test_digital_library_creation():
    dlib = DigitalLibrary("Digital Test", max_digital_copies=5)

    assert dlib.name == "Digital Test"
    assert dlib.max_digital_copies == 5
    assert "DigitalLibrary" in repr(dlib)


def test_digital_library_digital_copies():
    dlib = DigitalLibrary("Digital Test")
    book = Book("E-Book", "E-Author", 2023, "E-Genre", "123")

    dlib.add_digital_copy(book, copies=3)
    assert dlib._digital_copies["123"] == 3
    assert len(dlib) == 1

    result1 = dlib.borrow_book("123", "Reader 1")
    assert result1 is True
    assert dlib._digital_copies["123"] == 2

    result2 = dlib.borrow_book("123", "Reader 2")
    assert result2 is True
    assert dlib._digital_copies["123"] == 1

    result = dlib.return_book("123")
    assert result is True
    assert dlib._digital_copies["123"] == 2

    dlib.add_digital_copy(book, copies=998)
    assert dlib._digital_copies["123"] == dlib.max_digital_copies


def test_digital_library_multiple_borrow():
    dlib = DigitalLibrary("Digital Test")
    book = Book("E-Book", "E-Author", 2023, "E-Genre", "123")
    dlib.add_digital_copy(book, copies=2)

    # Оба читателя могут получить книгу одновременно
    assert dlib.borrow_book("123", "Reader 1") is True
    assert dlib.borrow_book("123", "Reader 2") is True

    # Третий читатель не может получить (копии кончились)
    assert dlib.borrow_book("123", "Reader 3") is False