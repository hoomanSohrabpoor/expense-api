# Expense Management API

A simple CRUD API for managing expenses, built with **FastAPI**.  
Expenses are stored in memory using a Python dictionary (no database required).

## Features

- Create a new expense with an auto-generated unique ID
- Retrieve all expenses
- Retrieve a single expense by ID
- Update an existing expense
- Delete an expense
- Returns proper HTTP status codes (including `404` when an expense is not found)

## Endpoints

| Method | Endpoint | Description |
|--------|-----------------------|----------------------------|
| POST   | `/expenses`           | Create a new expense       |
| GET    | `/expenses`           | Get all expenses           |
| GET    | `/expenses/{id}`      | Get a single expense by ID |
| PUT    | `/expenses/{id}`      | Update an expense by ID    |
| DELETE | `/expenses/{id}`      | Delete an expense by ID    |

## Expense Model

```json
{
  "id": 1,
  "description": "lunch",
  "amount": 25.5
}