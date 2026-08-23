from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

expenses = {}
next_id = 1

class Expense(BaseModel):
    description: str
    amount: float


@app.post("/expenses", status_code=201)
def create_expense(expense: Expense):
    global next_id
    new_expense = {
        "id": next_id,
        "description": expense.description,
        "amount": expense.amount
    }
    expenses[next_id] = new_expense
    next_id += 1
    return new_expense


@app.get("/expenses")
def get_all_expenses():
    return list(expenses.values())


@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expenses[expense_id]


@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: Expense):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    expenses[expense_id] = {
        "id": expense_id,
        "description": expense.description,
        "amount": expense.amount
    }
    return expenses[expense_id]


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    del expenses[expense_id]
    return {"detail": "Expense deleted successfully"}