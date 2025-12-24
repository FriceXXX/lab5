import random
import sys

from src.Library.library import Library
from src.Library.book import Book
from src.samples import SAMPLE_BOOKS, AUTHORS, YEARS, READERS, GENRES

def terminal():
    library = Library("Центральная городская библиотека")

    while True:

        user_input = input().split()
        cmd = user_input[0]
        args = user_input[1:]
        if cmd == 'q':
            sys.exit()
        if cmd == 'add':
            if len(args) != 5:
                print("Not enough arguments")
            else:
                book = Book(args[0], args[1], args[2], args[3], args[4])
                if book not in library:
                    library.add_book(book)
                    print(f"Добавлена новая книга: {book}")
                else:
                    print(f"Попытка добавить существующую книгу: {book.title}")
        if cmd == 'remove':
