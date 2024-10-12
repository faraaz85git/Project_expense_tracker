from fastapi import HTTPException
from starlette import status
from datetime import datetime
class InvalidDate(Exception):
    def __init__(self, message: str = "Invalid date. It should be in YYYY-MM-DD format."):
        self.message = message  # Ensure the message is stored in the instance
        super().__init__(self.message)

class InvalidCategory(Exception):
    def __init__(self,message=f"Category is unacceptable.it must be one of [transport,housing,food,clothing,other]"):
        self.message = message
        super().__init__(self.message)
def validate_expense(expense):
    try:
        datetime.strptime(expense.date,"%Y-%m-%d")
    except Exception:
        raise InvalidDate()
    categories=["housing","transport","food","shopping","other"]
    if expense.category not in categories:
        raise InvalidCategory()