# RefVault

A lightweight API for storing and organizing image reference URLs with tags.

## Features

- Store image URLs with names
- Tag images with flexible labels
- Retrieve and update images
- Simple REST API
- Async FastAPI backend
- PostgreSQL database
- Dockerized setup

## Quick Start

API: http://localhost:8000  
Docs: http://localhost:8000/docs

```bash
make up
```

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- Alembic
- Docker

## Testing

```
pytest
```

## Roadmap

**Planned:**

- [ ] Add pagination
- [ ] Add search by name and tags
- [ ] Improve test coverage

**Possible ideas:**

- [ ] Add user
- [ ] Add collections
- [ ] Add upload
- [ ] Add caching
