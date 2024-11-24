import uuid
from dataclasses import field, dataclass
from enum import Enum


class BookStatus(Enum):
    """
    Статус книги.
    """
    AVAILABLE = "в наличии"
    ISSUED = "выдана"

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def from_str(value: str) -> "BookStatus":
        """
        Преобразует строку в объект BookStatus.
        """
        for status in BookStatus:
            if status.value == value:
                return status
        raise ValueError("Неверный статус книги")


@dataclass
class Book:
    """
    Класс для представления книги.
    """
    title: str
    author: str
    year: int
    status: BookStatus = BookStatus.AVAILABLE
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        """
        Преобразует объект книги в словарь.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": str(self.status),
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        """
        Создает объект книги из словаря.
        """
        return Book(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=BookStatus(data["status"]),
        )
