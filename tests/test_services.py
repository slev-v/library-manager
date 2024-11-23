from unittest import TestCase
from unittest.mock import MagicMock

from src.models import Book, BookStatus
from src.services import LibraryService


class TestLibraryService(TestCase):
    def setUp(self) -> None:
        self.mock_storage = MagicMock()
        self.service = LibraryService(storage=self.mock_storage)

    def test_add_book(self) -> None:
        self.mock_storage.load_books.return_value = []

        self.service.add_book("Test Book", "Author", 1999)

        self.mock_storage.save_books.assert_called_once()
        saved_books = self.mock_storage.save_books.call_args[0][0]
        self.assertEqual(len(saved_books), 1)
        self.assertEqual(saved_books[0].title, "Test Book")

    def test_remove_book(self) -> None:
        book = Book("Test Book", "Author", 1999)
        self.mock_storage.load_books.return_value = [book]

        self.service.remove_book(book.id)
        self.mock_storage.save_books.assert_called_once()

    def test_remove_non_existent_book(self) -> None:
        self.mock_storage.load_books.return_value = []

        with self.assertRaises(ValueError):
            self.service.remove_book("none_existent_id")

    def test_search_books_by_title(self) -> None:
        books = [
            Book(title="Python Basics", author="John", year=2020),
            Book(title="Advanced Python", author="Margo", year=2021),
        ]
        self.mock_storage.load_books.return_value = books

        result = self.service.search_books(title="Python")
        self.assertEqual(len(result), 2)

        result = self.service.search_books(title="Advanced")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Advanced Python")

    def test_search_books_by_author(self) -> None:
        books = [
            Book(title="Python Basics", author="John", year=2020),
            Book(title="Advanced Python", author="Margo", year=2021),
        ]
        self.mock_storage.load_books.return_value = books

        result = self.service.search_books(author="John")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].author, "John")

    def test_search_books_by_year(self) -> None:
        books = [
            Book(title="Python Basics", author="John", year=2020),
            Book(title="Advanced Python", author="Margo", year=2021),
        ]
        self.mock_storage.load_books.return_value = books

        result = self.service.search_books(year=2020)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].year, 2020)

    def test_search_books_combined_filters(self) -> None:
        books = [
            Book(title="Python Basics", author="John", year=2020),
            Book(title="Advanced Python", author="Margo", year=2021),
        ]
        self.mock_storage.load_books.return_value = books

        result = self.service.search_books(title="Python", author="Margo")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Advanced Python")

    def test_get_all_books(self) -> None:
        books = [
            Book(title="Book 1", author="Author 1", year=2020),
            Book(title="Book 2", author="Author 2", year=2021),
        ]
        self.mock_storage.load_books.return_value = books

        result = self.service.get_all_books()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Book 1")
        self.assertEqual(result[1].title, "Book 2")

        self.mock_storage.load_books.assert_called_once()

    def test_update_book_status_success(self) -> None:
        book = Book("Test Book", "Author", 1999)
        self.mock_storage.load_books.return_value = [book]

        self.service.update_book_status(book.id, "выдана")

        self.assertEqual(book.status, BookStatus.ISSUED)
        self.mock_storage.save_books.assert_called_once()

    def test_update_book_status_invalid_id(self) -> None:
        self.mock_storage.load_books.return_value = []

        with self.assertRaises(ValueError) as context:
            self.service.update_book_status("invalid_id", "выдана")

        self.assertEqual(str(context.exception), "Книга не найдена")

        self.mock_storage.save_books.assert_not_called()

    def test_update_book_status_invalid_status(self) -> None:
        book = Book(title="Test Book", author="Author", year=1999)
        self.mock_storage.load_books.return_value = [book]

        with self.assertRaises(ValueError):
            self.service.update_book_status(book.id, "invalid_status")

        self.assertNotEqual(book.status, "Неверный статус книги")
        self.mock_storage.save_books.assert_not_called()
