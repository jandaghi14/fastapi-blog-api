[![CI](https://github.com/jandaghi14/fastapi-blog-api/actions/workflows/ci.yml/badge.svg)](https://github.com/jandaghi14/fastapi-blog-api/actions/workflows/ci.yml)
# fastapi-blog-api

[![GitHub](https://img.shields.io/badge/GitHub-jandaghi14-181717?logo=github)](https://github.com/jandaghi14)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ali%20Jandaghi-0077B5?logo=linkedin)](https://www.linkedin.com/in/ali-jandaghi-9a3188b1)

A production-structured blog REST API built with **FastAPI**, **async SQLAlchemy**, and **PostgreSQL**. Designed as a portfolio project demonstrating clean layered architecture, JWT authentication, role-based access control, and a comprehensive test suite.

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Features](#features)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Running the App](#running-the-app)
- [Database Migrations](#database-migrations)
- [Running Tests](#running-tests)
- [Design Decisions](#design-decisions)

---

## Overview

`fastapi-blog-api` is a fully async blog backend API that supports user registration and authentication, blog post management with pagination, a comment system, a tag system with many-to-many post relationships, and title/tag search with OR logic. The project follows a strict three-layer architecture (repositories → services → routers) and is covered by an isolated async test suite using a dedicated test database.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy (async) |
| Database | PostgreSQL |
| Migrations | Alembic |
| Auth | JWT via `python-jose` |
| Password hashing | `passlib` + `bcrypt` |
| Validation | Pydantic v2 |
| Rate limiting | `slowapi` |
| Testing | `pytest`, `pytest-asyncio`, `httpx` |
| Settings | `pydantic-settings` |
| Logging | Python `logging` (console + file) |

---

## Project Structure

```
fastapi-blog-api/
├── app/
│   ├── main.py                  # App factory, middleware, exception handlers
│   ├── db/
│   │   ├── base.py              # SQLAlchemy declarative Base
│   │   ├── session.py           # Async engine and session factory
│   │   └── all_models.py        # Imports all models (for Alembic discovery)
│   ├── core/
│   │   ├── config.py            # Settings from .env (pydantic-settings)
│   │   ├── enums.py             # Role enum (user / admin)
│   │   ├── security.py          # Password hashing and verification
│   │   ├── jwt.py               # Token creation and decoding
│   │   ├── dependencies.py      # FastAPI dependency: get_current_user
│   │   ├── exceptions.py        # Custom exception classes
│   │   ├── logger.py            # Structured logger (console + file)
│   │   └── limiter.py           # slowapi rate limiter instance
│   ├── models/
│   │   ├── model_user.py
│   │   ├── model_post.py
│   │   ├── model_comment.py
│   │   ├── model_tag.py
│   │   └── model_post_tag.py    # Association table (many-to-many)
│   ├── schemas/
│   │   ├── scheme_user.py
│   │   ├── scheme_post.py
│   │   ├── scheme_comment.py
│   │   └── scheme_tag.py
│   ├── repositories/
│   │   ├── base_repository.py   # Abstract base (create/get/update/delete)
│   │   ├── user_repository.py
│   │   ├── post_repository.py
│   │   ├── comment_repository.py
│   │   ├── tag_repository.py
│   │   └── post_tag_repository.py
│   ├── services/
│   │   ├── service_user.py
│   │   ├── service_post.py
│   │   ├── service_comment.py
│   │   └── service_tag.py
│   └── routers/
│       ├── router_auth.py
│       ├── router_post.py
│       ├── router_comment.py
│       └── router_tag.py
├── alembic/
│   └── versions/
├── tests/
│   ├── conftest.py
│   ├── test_router_auth.py
│   ├── test_router_post.py
│   ├── test_router_comment.py
│   ├── test_router_tag.py
│   
├── .env
├── alembic.ini
├── pytest.ini
└── requirements.txt
```

---

## Architecture

The project follows a strict **three-layer architecture**:

```
Router  →  Service  →  Repository  →  Database
```

- **Routers** handle HTTP concerns only: request parsing, response codes, and exception mapping.
- **Services** contain business logic: ownership checks, validation, orchestration across multiple repositories.
- **Repositories** handle all database queries. Each extends an abstract `BaseRepository` enforcing a consistent interface.

This separation means database logic is never in routers, and HTTP logic never leaks into services.

---

## Features

- **User auth**: Registration, login with JWT bearer tokens, rate-limited login (5/minute)
- **Role-based access**: `user` and `admin` roles; admins can update or delete any post
- **Posts**: Create, read, update, delete with ownership enforcement
- **Pagination**: All posts endpoint returns `total`, `page`, `pages`, `size`, and `items`
- **Search**: Filter posts by `title` (ILIKE) and/or `is_published`. Basic search filters within published status; advanced search crosses title and tag names with OR logic.
- **Tag + title search**: OR logic across post titles and tag names using a LEFT OUTER JOIN with `.distinct()` to avoid duplicates
- **Comments**: Full CRUD, scoped to post existence and comment ownership
- **Tags**: Create, read, update, delete; many-to-many assignment to posts
- **Logging**: Every request logged with method, path, and response time; post creation logged at service and repository level
- **CORS**: Open (`*`) for development.In production this should be restricted to specific origins
- **Global exception handlers**: Custom `NotFoundException`, `UnauthorizedException`, `AlreadyExistsException` map to clean JSON error responses

---

## Database Models

| Model | Table | Key Fields |
|---|---|---|
| `User` | `users` | `id`, `username`, `email`, `password`, `role`, `is_active` |
| `Post` | `posts` | `id`, `title`, `content`, `created_at`, `is_published`, `owner_id` |
| `Comment` | `comments` | `id`, `content`, `created_at`, `is_published`, `owner_id`, `post_id` |
| `Tag` | `tags` | `id`, `name` |
| `PostTag` | `posts_tags` | `post_id` (PK), `tag_id` (PK) |

`Post` ↔ `Tag` is a many-to-many relationship via the `posts_tags` association table, declared with SQLAlchemy `relationship` and `secondary`.

---

## API Endpoints

### Auth — `/auth`

| Method | Path | Description |
|---|---|---|
| POST | `/auth/user_register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT (rate limited: 5/min) |
| POST | `/auth/user/promote/{user_id}` | Promote user to admin (admin only) |

### Posts — `/post`

| Method | Path | Description |
|---|---|---|
| POST | `/post/create_post` | Create a post |
| GET | `/post/get_all_posts` | Get all posts (paginated: `page`, `size`) |
| GET | `/post/get_post_by_id/{post_id}` | Get a single post |
| GET | `/post/search` | Search by `title` and/or `is_published` |
| GET | `/post/search_tag_title` | Search by `title` OR `tag` (OR logic, distinct) |
| PUT | `/post/update_post/{post_id}` | Update a post (owner or admin) |
| DELETE | `/post/delete_post/{post_id}` | Delete a post (owner or admin) |

### Comments — `/comment`

| Method | Path | Description |
|---|---|---|
| POST | `/comment/create_comment` | Create a comment on a post |
| GET | `/comment/get_by_id/{comment_id}` | Get comment by ID |
| GET | `/comment/get_by_post_id/{post_id}` | Get all comments on a post |
| PUT | `/comment/update/{comment_id}` | Update a comment (owner only) |
| DELETE | `/comment/delete/{comment_id}` | Delete a comment (owner only) |

### Tags — `/tag`

| Method | Path | Description |
|---|---|---|
| POST | `/tag/create_tag` | Create a tag |
| GET | `/tag/get_all` | List all tags |
| GET | `/tag/get_by_id/{tag_id}` | Get tag by ID |
| PUT | `/tag/update` | Update tag name |
| DELETE | `/tag/delete/{tag_id}` | Delete a tag |
| POST | `/tag/assign_tag_to_post` | Assign a tag to a post |
| DELETE | `/tag/remove_tag_from_post` | Remove a tag from a post |

---

## Setup & Installation

**Prerequisites**: Python 3.12+, PostgreSQL

```bash
# Clone the repository
git clone https://github.com/jandaghi14/fastapi-blog-api.git
cd fastapi-blog-api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/blog_db
TEST_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/blog_test_db

JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_DEFAULT_TIME_EXPIRE=30
```

---

## Running the App

```bash
uvicorn app.main:app --reload
```

Interactive API docs available at `http://localhost:8000/docs`.

---

## Database Migrations

```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "your message"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

---

## Running Tests

The test suite runs against a **dedicated test database** (isolated from development data). Tables are truncated with `RESTART IDENTITY CASCADE` after each test to guarantee isolation.

```bash
pytest
```

All **55 tests pass** (`55 passed, 1 warning in ~35s`):

| File | Tests |
|---|---|
| `test_router_auth.py` | 6 |
| `test_router_comment.py` | 14 |
| `test_router_post.py` | 19 |
| `test_router_tag.py` | 15 |
| **Total** | **55** |

Coverage includes:

- Auth: registration, login (success, wrong username, wrong password), rate limiting (429)
- Posts: CRUD, pagination, ownership enforcement, admin override, search by title/published, search by title+tag with OR logic
- Comments: CRUD, post existence check, ownership enforcement, cross-user access
- Tags: CRUD, duplicate prevention, assign/remove from post, not-found edge cases

---

## Design Decisions

**Async throughout** — `create_async_engine`, `async_sessionmaker`, and `AsyncSession` are used end-to-end to keep I/O non-blocking.

**Abstract base repository** — `BaseRepository` enforces a consistent interface across all repositories, making the data layer predictable and extendable.

**Service layer owns business logic** — ownership checks, role validation, and multi-repository orchestration all live in services, keeping routers thin.

**Custom exceptions over HTTPException in services** — `NotFoundException`, `UnauthorizedException`, and `AlreadyExistsException` are raised in services and mapped to HTTP responses in `main.py`, keeping HTTP concerns out of business logic.

**OR search with OUTER JOIN and DISTINCT** — `search_tag_title` uses `outerjoin(Post.tags)` so posts without any tags are still matched by title, combined with `or_()` and `.distinct()` to prevent duplicate results when a post has multiple matching tags.

**Test isolation via TRUNCATE** — Rather than rolling back transactions, each test gets a clean database state through a `TRUNCATE ... RESTART IDENTITY CASCADE` after teardown, matching production-like commit behaviour.
