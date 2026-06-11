# 🧪 runtime-tool

Gerador de scaffolding de projetos. Sofre uma vez, usa pra sempre.

Monta a estrutura completa de um projeto (runtime, banco de dados, arquitetura) com Docker pronto pra subir em segundos. Quanto mais alimentado com templates, mais versátil fica.

---

## Pré-requisitos

- Python 3.10+
- [Docker](https://docs.docker.com/get-docker/) + [Docker Compose](https://docs.docker.com/compose/install/)

---

## Instalação

```bash
git clone https://github.com/rufatto-dotcom/runtime-tool
cd runtime-tool
pip install -r requirements.txt
```

**Dependências:**
```
questionary
```

---

## Como usar

### Modo interativo

```bash
python main.py
```

Abre um menu guiado para escolher linguagem, banco de dados, arquitetura e nome do projeto.

### Modo CLI

```bash
python main.py new --runtime python --name meu-projeto
```

```bash
python main.py new --runtime php --name minha-api --architecture orm --database MySQL PostgreSQL
```

**Parâmetros disponíveis:**

| Parâmetro | Obrigatório | Descrição |
|---|---|---|
| `--runtime` | ✅ | `python`, `php`, `java` |
| `--name` | ✅ | Nome da pasta do projeto |
| `--architecture` | ❌ | `orm`, `webserver` |
| `--database` | ❌ | `MySQL`, `PostgreSQL` (pode passar mais de um) |

---

## Estrutura

```
runtime-tool/
├── main.py              # Entrypoint (CLI + interativo)
├── core.py              # Lógica principal
├── interactive.py       # Menu interativo (questionary)
├── runtimes/            # Templates base por linguagem
│   ├── python/
│   ├── php/
│   └── java/
└── architectures/       # Camadas arquiteturais opcionais
    ├── orm/
    └── webserver/
```

### Como os templates funcionam

Os arquivos dentro de `runtimes/` e `architectures/` podem conter variáveis no formato `{{VARIAVEL}}`.
Elas são substituídas automaticamente ao criar o projeto.

**Variáveis disponíveis:**

| Variável | Exemplo |
|---|---|
| `{{PROJECT_NAME}}` | `meu-projeto` |
| `{{RUNTIME}}` | `python` |
| `{{RUNTIME_IMAGE}}` | `python:3.13` |
| `{{ARCHITECTURE}}` | `orm` |
| `{{DATABASES}}` | `MySQL, PostgreSQL` |
| `{{COMPOSE_SERVICES}}` | bloco YAML dos serviços docker-compose |

---

## Runtimes suportados

| Runtime | Imagem Docker |
|---|---|
| Python | `python:3.13` |
| PHP | `php:8.4-cli` |
| Java | `eclipse-temurin:21` |

---

## Bancos de dados suportados

| Banco | Versão |
|---|---|
| MySQL | 8.4 |
| PostgreSQL | 16 |

---

## Roadmap

- [ ] Benchmarks entre runtimes
- [ ] Suporte a MongoDB, Redis
- [ ] `python_lab list` — listar projetos criados
- [ ] Geração de `project.json` por projeto
- [ ] Mais arquiteturas (Clean Architecture, MVC)

---

## Beta

Esta é uma versão Beta. Novos runtimes, arquiteturas e bancos de dados serão adicionados com o tempo.
Pull requests e sugestões são bem-vindos.
