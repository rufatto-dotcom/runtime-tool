import shutil
from pathlib import Path

TEXT_EXTENSIONS = {
    ".py", ".php", ".java", ".js", ".ts", ".html", ".css",
    ".yaml", ".yml", ".json", ".xml", ".toml", ".ini",
    ".env", ".md", ".txt", ".sh", ".dockerfile", ".conf"
}

RUNTIME_IMAGES = {
    "python": "python:3.13",
    "php": "php:8.4-cli",
    "java": "eclipse-temurin:21",
}

DATABASE_SERVICES = {
    "MySQL": """
  mysql:
    image: mysql:8.4
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: app
    ports:
      - "3306:3306"
""",
    "PostgreSQL": """
  postgres:
    image: postgres:16
    restart: always
    environment:
      POSTGRES_PASSWORD: root
      POSTGRES_DB: app
    ports:
      - "5432:5432"
""",
}

def get_runtime_image(runtime: str) -> str:
    image = RUNTIME_IMAGES.get(runtime.lower())
    if not image:
        raise ValueError(f"Runtime '{runtime}' não suportado. Disponíveis: {list(RUNTIME_IMAGES.keys())}")
    return image


def build_compose_services(databases: list[str]) -> str:
    services = [DATABASE_SERVICES[db] for db in databases if db in DATABASE_SERVICES]
    return "\n".join(services)


def build_context(runtime: str, architecture: str, databases: list[str], project_name: str) -> dict:
    return {
        "PROJECT_NAME": project_name,
        "RUNTIME": runtime,
        "ARCHITECTURE": architecture or "",
        "DATABASES": ", ".join(databases),
        "RUNTIME_IMAGE": get_runtime_image(runtime),
        "COMPOSE_SERVICES": build_compose_services(databases),
    }


def process_templates(project_path: Path, variables: dict) -> None:
    for file in project_path.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            content = file.read_text(encoding="utf-8")
            for key, value in variables.items():
                content = content.replace(f"{{{{{key}}}}}", str(value))
            file.write_text(content, encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            pass  # silently skip unreadable files


def create_project(runtime: str, architecture: str | None, databases: list[str], project_name: str) -> dict:
    """
    Creates a new project from templates.
    Returns a result dict with 'success' and 'message'.
    """
    parent_folder = Path(project_name)

    if parent_folder.exists():
        return {"success": False, "message": f"Projeto '{project_name}' já existe."}

    runtime_path = Path(f"runtimes/{runtime.lower()}")
    if not runtime_path.exists():
        return {"success": False, "message": f"Runtime '{runtime}' não encontrado em {runtime_path}."}

    shutil.copytree(runtime_path, parent_folder, dirs_exist_ok=True)

    if architecture:
        arch_path = Path(f"architectures/{architecture.lower()}/{runtime.lower()}")
        if arch_path.exists():
            shutil.copytree(arch_path, parent_folder / "src", dirs_exist_ok=True)
        else:
            print(f"⚠️  Arquitetura '{architecture}' não encontrada para '{runtime}'. Pulando.")

    context = build_context(runtime, architecture, databases, project_name)
    process_templates(parent_folder, context)

    return {"success": True, "message": f"✅ Projeto '{project_name}' criado com sucesso!"}