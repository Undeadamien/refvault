# RefVault

A lightweight API for storing and organizing image reference URLs with tags.

## Features

- JWT authentication with user-scoped data
- Store image URLs with names and tags
- Full CRUD for images
- Async FastAPI + PostgreSQL + Docker

## Quick Start

```bash
make up
```

API at http://localhost:8000, docs at http://localhost:8000/docs.

## Testing

```bash
pytest
```

## Roadmap

- [ ] Pagination
- [ ] Search by name and tags
- [ ] User registration endpoint
