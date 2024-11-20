from storage import Storage
from models import Book, BookStatus


class LibraryService:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def add_book(self, title: str, author: str, year: int) -> None:
        books = self.storage.load_books()
        new_book = Book(title=title, author=author, year=year)
        books.append(new_book)
        self.storage.save_books(books)

    def remove_book(self, book_id: str) -> None:
        books = self.storage.load_books()
        filtered_books = [book for book in books if book.id != book_id]

        if len(books) == len(filtered_books):
            raise ValueError("Книга не найдена")

        self.storage.save_books(filtered_books)

    def search_books(
        self,
        title: str | None = None,
        author: str | None = None,
        year: int | None = None,
    ) -> list[Book]:
        books = self.storage.load_books()
        results = books

        if title:
            results = [book for book in results if title.lower() in book.title.lower()]
        if author:
            results = [
                book for book in results if author.lower() in book.author.lower()
            ]
        if year:
            results = [book for book in results if year == book.year]

        return results

    def get_all_books(self) -> list[Book]:
        return self.storage.load_books()

    def update_book_status(self, book_id: str, status: str) -> None:
        books = self.storage.load_books()
        for book in books:
            if book.id == book_id:
                book.status = BookStatus.from_str(status)
                self.storage.save_books(books)
                break
        else:
            raise ValueError("Книга не найдена")
