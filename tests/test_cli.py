from unittest import TestCase
from unittest.mock import MagicMock

from src.services import LibraryService
from src.cli import setup_parser, execute_command


class TestSetupParser(TestCase):
    def setUp(self) -> None:
        self.parser = setup_parser()

    def test_add_command(self) -> None:
        args = self.parser.parse_args(
            ["add", "--title", "Book", "--author", "Author", "--year", "1999"]
        )
        self.assertEqual(args.command, "add")
        self.assertEqual(args.title, "Book")
        self.assertEqual(args.author, "Author")
        self.assertEqual(args.year, 1999)

    def test_remove_command(self) -> None:
        args = self.parser.parse_args(["remove", "--id", "12345"])
        self.assertEqual(args.command, "remove")
        self.assertEqual(args.id, "12345")

    def test_search_command(self) -> None:
        args = self.parser.parse_args(["search", "--title", "Book"])
        self.assertEqual(args.command, "search")
        self.assertEqual(args.title, "Book")
        self.assertIsNone(args.author)
        self.assertIsNone(args.year)

    def test_list_command(self) -> None:
        args = self.parser.parse_args(["list"])
        self.assertEqual(args.command, "list")

    def test_update_command(self) -> None:
        args = self.parser.parse_args(
            ["update", "--id", "12345", "--status", "в наличии"]
        )
        self.assertEqual(args.command, "update")
        self.assertEqual(args.id, "12345")
        self.assertEqual(args.status, "в наличии")


class TestExecuteCommand(TestCase):
    def setUp(self) -> None:
        self.library_service = MagicMock(spec=LibraryService)

    def test_add_command(self) -> None:
        args = MagicMock()
        args.command = "add"
        args.title = "Book"
        args.author = "Author"
        args.year = 1999

        execute_command(args, self.library_service)

        self.library_service.add_book.assert_called_once_with("Book", "Author", 1999)

    def test_remove_command(self) -> None:
        args = MagicMock()
        args.command = "remove"
        args.id = "12345"

        execute_command(args, self.library_service)

        self.library_service.remove_book.assert_called_once_with("12345")

    def test_search_command(self) -> None:
        args = MagicMock()
        args.command = "search"
        args.title = "Book"
        args.author = None
        args.year = None

        execute_command(args, self.library_service)

        self.library_service.search_books.assert_called_once_with("Book", None, None)

    def test_list_command(self) -> None:
        args = MagicMock()
        args.command = "list"

        execute_command(args, self.library_service)

        self.library_service.get_all_books.assert_called_once()

    def test_update_command(self) -> None:
        args = MagicMock()
        args.command = "update"
        args.id = "12345"
        args.status = "в наличии"

        execute_command(args, self.library_service)

        self.library_service.update_book_status.assert_called_once_with(
            "12345", "в наличии"
        )
