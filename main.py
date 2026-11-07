from fastapi import FastAPI, HTTPException, Response, Request, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from i18n import get_translator
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

expenses = {}
next_id = 1

@app.get("/")
def home(_=Depends(get_translator)):
    return {"message": _("Welcome to the Expense API")}

class ExpenseIn(BaseModel):
    description: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    category: str = Field(pattern=r"^[a-zA-Z]+$")


class ExpenseOut(BaseModel):
    id: int
    description: str
    amount: float
    category: str

class UserRegister(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


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
def get_expense(expense_id: int, _=Depends(get_translator)):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail=_("Expense not found"))
    return expenses[expense_id]


@app.put("/expenses/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, expense: ExpenseIn, _=Depends(get_translator)):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail=_("Expense not found"))
    expenses[expense_id] = {
        "id": expense_id,
        "description": expense.description,
        "amount": expense.amount,
        "category": expense.category,
    }
    return expenses[expense_id]


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, _=Depends(get_translator)):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail=_("Expense not found"))
    del expenses[expense_id]
    return {"detail": _("Expense deleted successfully")}

@app.post("/register", status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db), _=Depends(get_translator)):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail=_("Username already taken"))

    user = User(
        name=data.name,
        username=data.username,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}
@app.post("/login")
def login(data: UserLogin, response: Response, db: Session = Depends(get_db), _=Depends(get_translator)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail=_("Invalid username or password"))

    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/refresh",
    )

    return {"detail": _("Login successful")}

@app.post("/refresh")
def refresh(request: Request, response: Response, _=Depends(get_translator)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail=_("Refresh token missing"))

    payload = decode_token(token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail=_("Invalid or expired refresh token"))

    new_access_token = create_access_token(payload["sub"])

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"detail": _("Access token refreshed")}

@app.post("/logout")
def logout(response: Response, _=Depends(get_translator)):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token", path="/refresh")
    return {"detail": _("Logout successful")}