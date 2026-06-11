import questionary
from core import create_project, RUNTIME_IMAGES, DATABASE_SERVICES


def run_interactive():
    action = questionary.select(
        "O que deseja fazer?",
        choices=["Novo Projeto", "Benchmarks"],
    ).ask()

    if action == "Benchmarks":
        print("🚧 Em breve...")
        return

    runtime = questionary.select(
        "Escolha uma linguagem:",
        choices=[r.capitalize() for r in RUNTIME_IMAGES.keys()],
    ).ask()

    databases = questionary.checkbox(
        "Escolha os bancos de dados:",
        choices=list(DATABASE_SERVICES.keys()),
    ).ask()

    architecture = questionary.select(
        "Escolha uma arquitetura:",
        choices=["ORM", "WebServer", "Nenhuma"],
    ).ask()

    if architecture == "Nenhuma":
        architecture = None

    project_name = questionary.text("Nome do projeto:").ask()

    result = create_project(runtime, architecture, databases, project_name)
    print(result["message"])