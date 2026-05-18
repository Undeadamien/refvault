# RefVault

![Python](https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FASTAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLALCHEMY-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/PYDANTIC-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/POSTGRESQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/DOCKER-2496ED?style=for-the-badge&logo=docker&logoColor=white)

A personal image vault API. Users register, log in, and store image URLs organized with tags. Built with FastAPI, PostgreSQL, SQLAlchemy, and Docker. **~98% test coverage.**

## Features

- JWT authentication with user-scoped data
- Store image URLs with names and tags
- Paginated browsing
- Tag management
- SQLAdmin panel for data management

## Quick Start

```bash
make up
```

- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Admin: `http://localhost:8000/admin`

## Testing

```bash
pytest --cov
```

See `Makefile` for all available commands.
