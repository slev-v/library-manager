from argparse import ArgumentParser
from src.services import LibraryService


def setup_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Система управления библиотекой")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    add_parser = subparsers.add_parser("add", help="Добавить книгу")
    add_parser.add_argument("--title", required=True, help="Название книги")
    add_parser.add_argument("--author", required=True, help="Автор книги")
    add_parser.add_argument("--year", required=True, type=int, help="Год издания")

    remove_parser = subparsers.add_parser("remove", help="Удалить книгу")
    remove_parser.add_argument("--id", required=True, help="ID книги для удаления")

    search_parser = subparsers.add_parser("search", help="Найти книги")
    search_parser.add_argument("--title", help="Название книги")
    search_parser.add_argument("--author", help="Автор книги")
    search_parser.add_argument("--year", type=int, help="Год издания")

    subparsers.add_parser("list", help="Отобразить все книги")

    update_parser = subparsers.add_parser("update", help="Обновить статус книги")
    update_parser.add_argument("--id", required=True, help="ID книги")
    update_parser.add_argument(
        "--status", required=True, choices=["в наличии", "выдана"], help="Новый статус"
    )

    return parser


def execute_command(args, library_service: LibraryService):
    try:
        if args.command == "add":
            library_service.add_book(args.title, args.author, args.year)
            print("Книга успешно добавлена.")

        elif args.command == "remove":
            library_service.remove_book(args.id)
            print("Книга успешно удалена.")

        elif args.command == "search":
            books = library_service.search_books(args.title, args.author, args.year)
            if books:
                for book in books:
                    print(book)
            else:
                print("Книги не найдены.")

        elif args.command == "list":
            books = library_service.get_all_books()
            if books:
                for book in books:
                    print(book)
            else:
                print("В библиотеке нет книг.")

        elif args.command == "update":
            library_service.update_book_status(args.id, args.status)
            print("Статус книги успешно обновлён.")

        else:
            print("Неизвестная команда.")
    except ValueError as e:
        print(f"Ошибка: {e}")
