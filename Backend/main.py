from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import uuid

app = FastAPI()

class Month(str, Enum):
    January = "January"
    February = "February"
    March = "March"
    April = "April"
    May = "May"
    June = "June"
    July = "July"
    August = "August"
    September = "September"
    October = "October"
    November = "November"
    December = "December"

class Expense(BaseModel):
    id: str
    month: Month
    amount: float
    description: str

expenses_db = [
    {"id": str(uuid.uuid4()), "month": Month.January, "amount": 100.0, "description": "Groceries"},
    {"id": str(uuid.uuid4()), "month": Month.January, "amount": 50.0, "description": "Transportation"},
    {"id": str(uuid.uuid4()), "month": Month.February, "amount": 200.0, "description": "Dinner with friends"},
]

# Create (POST): Add a new expense
@app.post("/expenses/", response_model=Expense, tags=["Expenses"])
async def add_expense(expense: Expense):
    expense.id = str(uuid.uuid4())
    expenses_db.append(expense.dict())
    return expense


# Read (GET): Retrieve expenses for a specific month
@app.get("/expenses/{month}", response_model=List[Expense], tags=["Expenses"])
async def get_expenses_by_month(month: Month):
    return [expense for expense in expenses_db if expense["month"] == month]

# Read (GET): Retrieve a specific expense by ID
@app.get("/expenses/{expense_id}", response_model=Expense, tags=["Expenses"])
async def get_expense_by_id(expense_id: int):
    for expense in expenses_db:
        if expense["id"] == expense_id:
            return expense
    raise HTTPException(status_code=404, detail="Expense not found")

# Update (PATCH): Update details of a specific expense
@app.patch("/expenses/{expense_id}", response_model=Expense, tags=["Expenses"])
async def update_expense(expense_id: int, expense: Expense):
    for idx, existing_expense in enumerate(expenses_db):
        if existing_expense["id"] == expense_id:
            expenses_db[idx] = expense.dict()
            return expense
    raise HTTPException(status_code=404, detail="Expense not found")

# Delete (DELETE): Delete a specific expense
@app.delete("/expenses/{expense_id}", tags=["Expenses"])
async def delete_expense(expense_id: int):
    for idx, expense in enumerate(expenses_db):
        if expense["id"] == expense_id:
            del expenses_db[idx]
            return {"message": "Expense deleted successfully"}
    raise HTTPException(status_code=404, detail="Expense not found")
