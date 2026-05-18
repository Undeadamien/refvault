# RefVault

A lightweight API for storing and organizing image reference URLs with tags.

## Features

- JWT authentication with user-scoped data
- User registration and login
- Store image URLs with names and tags
- Full CRUD for images
- Async FastAPI + PostgreSQL + Docker
- 100% test coverage

## Quick Start

```bash
make up
```

API at http://localhost:8000, docs at http://localhost:8000/docs.

## Testing

```bash
pytest --cov
```

## Roadmap

- [ ] Create a simple Typer client
- [ ] File upload
- [ ] Rework the tests
- [ ] Search by name and tags
