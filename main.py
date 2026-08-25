from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

expenses = {}
next_id = 1

class ExpenseIn(BaseModel):
    description: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    category: str = Field(pattern=r"^[a-zA-Z]+$")


class ExpenseOut(BaseModel):
    id: int
    description: str
    amount: float
    category: str


@app.post("/expenses", status_code=201, response_model=ExpenseOut)
def create_expense(expense: ExpenseIn):
    global next_id
    new_expense = {
        "id": next_id,
        "description": expense.description,
        "amount": expense.amount,
        "category": expense.category
    }
    expenses[next_id] = new_expense
    next_id += 1
    return new_expense


@app.get("/expenses", response_model=list[ExpenseOut])
def get_all_expenses():
    return list(expenses.values())


@app.get("/expenses/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expenses[expense_id]


@app.put("/expenses/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, expense: ExpenseIn):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    expenses[expense_id] = {
        "id": expense_id,
        "description": expense.description,
        "amount": expense.amount,
        "category": expense.category
    }
    return expenses[expense_id]


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    del expenses[expense_id]
    return {"detail": "Expense deleted successfully"}