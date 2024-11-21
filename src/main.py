from services import LibraryService
from storage import Storage
from cli import execute_command, setup_parser


def main():
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
