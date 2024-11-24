import tempfile
from unittest import TestCase

from src.storage import Storage
from src.models import Book


class TestStorage(TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.storage = Storage(self.temp_file.name)

    def tearDown(self):
        self.temp_file.close()

    def test_save_and_load_books(self):
        """
        Проверяет, что методы save_books и load_books работают корректно
        """
        books = [Book(title="Test Book", author="Author", year=1999)]
        self.storage.save_books(books)
        loaded_books = self.storage.load_books()
        self.assertEqual(len(loaded_books), 1)
        self.assertEqual(loaded_books[0].title, "Test Book")
