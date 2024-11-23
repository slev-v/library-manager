from src.services import LibraryService
from src.storage import Storage
from src.cli import execute_command, setup_parser


def main() -> None:
    storage = Storage("data/books.json")
    library_service = LibraryService(storage)

    parser = setup_parser()
    args = parser.parse_args()

    if args.command:
        execute_command(args, library_service)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
