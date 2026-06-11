import argparse
import sys
from core import create_project, RUNTIME_IMAGES, DATABASE_SERVICES
from interactive import run_interactive


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python_lab",
        description="Gerador de projetos com templates e configurações prontas.",
    )
    subparsers = parser.add_subparsers(dest="command")

    new_parser = subparsers.add_parser("new", help="Cria um novo projeto")
    new_parser.add_argument(
        "--runtime",
        required=True,
        choices=list(RUNTIME_IMAGES.keys()),
        help="Linguagem/runtime do projeto",
    )
    new_parser.add_argument(
        "--name",
        required=True,
        help="Nome do projeto (usado como nome da pasta)",
    )
    new_parser.add_argument(
        "--architecture",
        default=None,
        choices=["orm", "webserver"],
        help="Arquitetura base (opcional)",
    )
    new_parser.add_argument(
        "--database",
        nargs="*",
        default=[],
        choices=list(DATABASE_SERVICES.keys()),
        help="Bancos de dados a incluir (ex: MySQL PostgreSQL)",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "new":
        result = create_project(
            runtime=args.runtime,
            architecture=args.architecture,
            databases=args.database,
            project_name=args.name,
        )
        print(result["message"])
        sys.exit(0 if result["success"] else 1)
    else:
        run_interactive()


if __name__ == "__main__":
    main()