from argparse import ArgumentParser
from textwrap import shorten
from src.services import LibraryService


def setup_parser() -> ArgumentParser:
    """
    Создает и настраивает парсер аргументов командной строки
    """
    parser = ArgumentParser(description="Система управления библиотекой")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Парсер для добавления книги
    add_parser = subparsers.add_parser("add", help="Добавить книгу")
    add_parser.add_argument("--title", required=True, help="Название книги")
    add_parser.add_argument("--author", required=True, help="Автор книги")
    add_parser.add_argument("--year", required=True, type=int, help="Год издания")

    # Парсер для удаления книги
    remove_parser = subparsers.add_parser("remove", help="Удалить книгу")
    remove_parser.add_argument("--id", required=True, help="ID книги для удаления")

    # Парсер для поиска книг
    search_parser = subparsers.add_parser("search", help="Найти книги")
    search_parser.add_argument("--title", help="Название книги")
    search_parser.add_argument("--author", help="Автор книги")
    search_parser.add_argument("--year", type=int, help="Год издания")

    # Парсер для отображения всех книг
    subparsers.add_parser("list", help="Отобразить все книги")

    # Парсер для обновления статуса книги
    update_parser = subparsers.add_parser("update", help="Обновить статус книги")
    update_parser.add_argument("--id", required=True, help="ID книги")
    update_parser.add_argument(
        "--status", required=True, choices=["в наличии", "выдана"], help="Новый статус"
    )

    return parser


def execute_command(args, library_service: LibraryService) -> None:
    """
    Выполняет команду, переданную через аргументы командной строки
    """
    try:
        if args.command == "add":
            library_service.add_book(args.title, args.author, args.year)
            print("Книга успешно добавлена.")

        elif args.command == "remove":
            library_service.remove_book(args.id)
            print("Книга успешно удалена.")

        elif args.command == "search":
            books = library_service.search_books(args.title, args.author, args.year)
            print_books_table(books)

        elif args.command == "list":
            books = library_service.get_all_books()
            print_books_table(books)

        elif args.command == "update":
            library_service.update_book_status(args.id, args.status)
            print("Статус книги успешно обновлён.")

        else:
            print("Неизвестная команда.")
    except ValueError as e:
        print(f"Ошибка: {e}")


def print_books_table(books):
    """
    Форматированный вывод списка книг в виде таблицы.
    """
    if not books:
        print("Нет книг для отображения.")
        return

    # Ширина столбцов
    col_widths = {"ID": 36, "Название": 30, "Автор": 20, "Год": 6, "Статус": 10}

    # Заголовок
    header = f"| {'ID'.ljust(col_widths['ID'])} | {'Название'.ljust(col_widths['Название'])} | {'Автор'.ljust(col_widths['Автор'])} | {'Год'.ljust(col_widths['Год'])} | {'Статус'.ljust(col_widths['Статус'])} |"
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    # Вывод книг
    for book in books:
        print(
            f"| {book.id.ljust(col_widths['ID'])} "
            f"| {shorten(book.title, width=col_widths['Название'] - 1, placeholder='…').ljust(col_widths['Название'])} "
            f"| {shorten(book.author, width=col_widths['Автор'] - 1, placeholder='…').ljust(col_widths['Автор'])} "
            f"| {str(book.year).ljust(col_widths['Год'])} "
            f"| {str(book.status).ljust(col_widths['Статус'])} |"
        )

    print("-" * len(header))
