# Expense Management API

A simple CRUD API for managing expenses, built with **FastAPI** and **Pydantic**.  
Expenses are stored in memory using a Python dictionary (no database required).

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
  - Separate input (`ExpenseIn`) and output (`ExpenseOut`) models

## Endpoints

| Method | Endpoint | Description |
|--------|-----------------------|----------------------------|
| POST   | `/expenses`           | Create a new expense       |
| GET    | `/expenses`           | Get all expenses           |
| GET    | `/expenses/{id}`      | Get a single expense by ID |
| PUT    | `/expenses/{id}`      | Update an expense by ID    |
| DELETE | `/expenses/{id}`      | Delete an expense by ID    |

## Models

**Input (ExpenseIn):**
```json
{
  "description": "lunch",
  "amount": 25.5,
  "category": "food"
}