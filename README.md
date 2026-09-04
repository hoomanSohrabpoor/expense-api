 # Expense Management API

A CRUD API for managing expenses, built with **FastAPI**, **Pydantic**, **SQLAlchemy**, and **Alembic**.  
Data is stored in a real **SQLite** database with proper relational structure.

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

## Database Schema

The database structure is documented in the `docs/` folder:

- `docs/database-schema.drawio` (editable diagram)
- `docs/database-schema.png` (image)

### Tables

| Table        | Columns                                              |
|--------------|------------------------------------------------------|
| `users`      | id (PK), name                                        |
| `categories` | id (PK), name                                        |
| `expenses`   | id (PK), description, amount, user_id (FK), category_id (FK) |

## Project Structure
