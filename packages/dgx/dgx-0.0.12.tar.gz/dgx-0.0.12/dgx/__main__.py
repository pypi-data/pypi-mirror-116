from argparse import ArgumentParser
from .dgx import create_app, delete_app, my_dir

parser = ArgumentParser(description='Dealergeek Generator API Express', usage='DGX', )

parser.add_argument(
    "-d",
    "--delete",
    default=None,
    required=False,
    help="Delete the project",
)
parser.add_argument(
    "-c",
    "--create",
    default=None,
    required=False,
    help="Create a new api",
)
parser.add_argument(
    "-m",
    "--mdir",
    default=None,
    required=False,
    help="current directory",
)


def main():
    """
    Evalua los parametros
    """
    args = parser.parse_args()
    if args.create:
        create_app(args.create)
    elif args.delete:
        delete_app(args.delete)
    elif args.mdir:
        my_dir()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
