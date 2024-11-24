import json
from pathlib import Path

from src.models import Book


class Storage:
    def __init__(self, file_path: str) -> None:
        """
        Конструктор класса Storage.
        Принимает на вход путь к файлу, в котором будут храниться книги.
        Создает файл, если его нет.
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def save_books(self, books: list[Book]) -> None:
        """
        Принимает на вход список книг и сохраняет его в файл
        """
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                [book.to_dict() for book in books], file, ensure_ascii=False, indent=4
            )

    def load_books(self) -> list[Book]:
        """
        Чмтает список книг из файла и возвращает его
        """
        with self.file_path.open("r", encoding="utf-8") as file:
            return [Book.from_dict(book) for book in json.load(file)]
