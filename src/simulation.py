import random
from src.Library.library import Library
from src.samples import SAMPLE_BOOKS, AUTHORS, YEARS, READERS, GENRES

def run_simulation(seed: int = 20, steps: int  | None = None) -> None:
    if not seed is None:
        random.seed(seed)

    print(random.choice(SAMPLE_BOOKS))
    library = Library("Центральная городская библиотека")

    for n in range(9):
        book = random.choice(SAMPLE_BOOKS)
        library.add_book(book)
        print(f"ШАГ 0: Добавлена начальная книга: {book}")

    step = 1
    while step < steps:
        print(f"\nШАГ {step}")

        event = random.choice([
            "add_book",
            "remove_book",
            "search_books",
            "update_index",
            "borrow_book",
            "return_book",
            "check_nonexistent"
        ])

        print(event)

        if event == "add_book":
            book = random.choice(SAMPLE_BOOKS)
            if book not in library:
                library.add_book(book)
                print(f"Добавлена новая книга: {book}")
            else:
                print(f"Попытка добавить существующую книгу: {book.title}")

        elif event == "remove_book":
            book = library.get_random_book()
            if book:
                library.remove_book(book.isbn)
                print(f"Удалена книга: {book}")
            else:
                print("Нет книг для удаления")

        elif event == "search_books":
            search_type = random.choice(["author", "genre", "year"])

            if search_type == "author":
                author = random.choice(AUTHORS)
                results = library.search_books(author)
                print(f"Поиск по автору '{author}': найдено {len(results)} книг")

            elif search_type == "genre":
                genre = random.choice(GENRES)
                results = library.search_books(genre)
                print(f"Поиск по жанру '{genre}': найдено {len(results)} книг")

            else:  # year
                year = random.choice(YEARS)
                results = library.search_books(str(year))
                print(f"Поиск по году {year}: найдено {len(results)} книг")

        elif event == "update_index":
            library.update_index()
            print(f"Обновлены индексы: {library._index}")

        elif event == "borrow_book":
            book = library.get_random_book()
            if book:
                reader = random.choice(READERS)
                if library.borrow_book(book.isbn, reader):
                    print(f"Книга '{book.title}' выдана читателю {reader}")
                else:
                    print(f"Книга '{book.title}' не может быть выдана")
            else:
                print("Нет книг для выдачи")

        elif event == "return_book":
            if library._borrowed_books:
                isbn = random.choice(list(library._borrowed_books.keys()))
                if library.return_book(isbn):
                    print(f"Книга с ISBN {isbn} возвращена в библиотеку")
            else:
                print("Нет выданных книг для возврата")

        elif event == "check_nonexistent":
            fake_isbn = "000-0-00-000000-0"
            result = library.search_books(fake_isbn)
            print(f"Поиск несуществующей книги (ISBN: {fake_isbn}): найдено {len(result)} книг")

        print(f"Текущее состояние: Книг в библиотеке: {len(library)}, Выдано: {len(library._borrowed_books)}")

        step += 1
