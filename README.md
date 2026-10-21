# Expense Management API

A CRUD API for managing expenses, built with **FastAPI**, **Pydantic**, **SQLAlchemy**, and **Alembic**.  
Data is stored in a real **SQLite** database with proper relational structure.  
Authentication is handled with **JWT** tokens stored in **HttpOnly cookies**.

## Features

- Create a new expense with an auto-generated unique ID
- Retrieve all expenses
- Retrieve a single expense by ID
- Update an existing expense
- Delete an expense
- Returns proper HTTP status codes (including `404` when an expense is not found)
- **Input/output validation with Pydantic models**
  - `description`: required, 1–100 characters
  - `amount`: must be greater than 0
  - `category`: required, letters only (validated with regex)
- **Relational database with SQLAlchemy ORM**
  - `users`, `categories`, and `expenses` tables
  - One-to-Many relationships (a user has many expenses, a category has many expenses)
- **Database migrations managed with Alembic**
- **JWT authentication with HttpOnly cookies** (access + refresh tokens)

## Database Schema

The database structure is documented in the `docs/` folder:

- `docs/database-schema.drawio` (editable diagram)
- `docs/database-schema.png` (image)

### Tables

| Table        | Columns                                              |
|--------------|------------------------------------------------------|
| `users`      | id (PK), name, username, hashed_password             |
| `categories` | id (PK), name                                        |
| `expenses`   | id (PK), description, amount, user_id (FK), category_id (FK) |

## Project Structure

```
expense-api/
├── alembic/            # database migrations
├── docs/               # database schema diagram
├── main.py             # FastAPI app and endpoints
├── database.py         # database connection and session
├── models.py           # SQLAlchemy models (tables)
├── auth.py             # password hashing and JWT helpers
├── alembic.ini         # Alembic configuration
└── README.md
```

## Installation

```bash
pip install fastapi uvicorn sqlalchemy alembic "python-jose[cryptography]" "passlib[bcrypt]" "bcrypt==4.0.1"
```

## Database Setup

```bash
alembic upgrade head
```

## Running the App

```bash
uvicorn main:app --reload
```

Then open your browser at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Authentication (JWT + HttpOnly Cookies)

This project uses JWT-based authentication with tokens stored in **HttpOnly cookies**.

### Token Strategy

| Token | Lifetime | Purpose |
|---------------|------------|-----------------------------------------|
| Access Token | 15 minutes | Short-lived, used for regular API access |
| Refresh Token | 7 days | Long-lived, used only to renew the access token |

Short-lived access tokens limit the damage if a token is leaked, while the refresh token allows session renewal without forcing the user to log in again.

### Auth Endpoints

| Method | Endpoint | Description |
|--------|-------------|------------------------------------------|
| POST | `/register` | Create a new user (password is hashed) |
| POST | `/login` | Validate credentials, set auth cookies |
| POST | `/refresh` | Issue a new access token using the refresh token |
| POST | `/logout` | Clear both cookies |

### Why Cookies Instead of the Authorization Header?

- **XSS protection:** cookies are set with `HttpOnly`, so JavaScript cannot read them. A token stored in `localStorage` and sent via the `Authorization` header is fully readable by any injected script.
- **Automatic handling:** the browser attaches the cookie to requests automatically, so the token never has to pass through client-side JavaScript.
- **CSRF consideration:** cookies are sent automatically, which introduces CSRF risk. This is mitigated with `SameSite=lax`, and the refresh cookie is additionally scoped with `path=/refresh` so it is only sent to the endpoint that needs it.

### Cookie Security Settings

| Flag | Purpose |
|--------------------|-------------------------------------------------|
| `HttpOnly` | Blocks JavaScript access (XSS mitigation) |
| `Secure` | Cookie is only sent over HTTPS |
| `SameSite=lax` | Not sent on cross-site requests (CSRF mitigation) |
| `max_age` | Matches the token lifetime |
| `path=/refresh` | Limits the refresh token to the refresh endpoint |

### JWT Security Notes

- Passwords are hashed with **bcrypt** and never stored or returned in plain text.
- Each token carries a `type` claim (`access` / `refresh`) so an access token cannot be used to refresh a session.
- The `SECRET_KEY` must be kept secret and loaded from environment variables in production.
- Tokens are signed with `HS256`; any tampering invalidates the signature.

### Error Handling

| Situation | Status | Response |
|--------------------------------------|--------|-----------------------------------|
| Username already exists | `400` | `Username already taken` |
| Wrong username or password | `401` | `Invalid username or password` |
| Refresh cookie missing | `401` | `Refresh token missing` |
| Token expired, tampered, or wrong type | `401` | `Invalid or expired refresh token` |

Login errors intentionally use a single generic message so an attacker cannot determine whether a username exists.

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- SQLite
- JWT (python-jose)
- bcrypt (passlib)
