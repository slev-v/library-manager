from src.storage import Storage
from src.models import Book, BookStatus


class LibraryService:
    """
    Класс, предоставляющий методы для работы с библиотекой
    """

    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет новую книгу в библиотеку
        """
        books = self.storage.load_books()
        new_book = Book(title=title, author=author, year=year)
        books.append(new_book)
        self.storage.save_books(books)

    def remove_book(self, book_id: str) -> None:
        """
        Удаляет книгу по её id
        """
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
        """
        Возвращает список книг, отфильтрованных по названию, автору и/или году издания
        """
        books = self.storage.load_books()

        def matches(book: Book) -> bool:
            """
            Проверяет, соответствует ли книга всем переданным критериям.
            """
            return all(
                [
                    title.lower() in book.title.lower() if title else True,
                    author.lower() in book.author.lower() if author else True,
                    year == book.year if year else True,
                ]
            )

        return list(filter(matches, books))

    def get_all_books(self) -> list[Book]:
        """
        Возвращает список всех книг
        """
        return self.storage.load_books()

    def update_book_status(self, book_id: str, status: str) -> None:
        """
        Обновляет статус книги по её id

        :status: ("в наличии", "выдана")
        """
        books = self.storage.load_books()
        for book in books:
            if book.id == book_id:
                book.status = BookStatus.from_str(status)
                self.storage.save_books(books)
                break
        else:
            raise ValueError("Книга не найдена")
