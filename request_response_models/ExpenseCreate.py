from pydantic import BaseModel,Field,field_validator
from typing import Optional
from datetime import datetime


class ExpenseCreate(BaseModel):
    date: str = Field(description="Date must be in YYYY-MM-DD format.")
    category: str = Field(description="Category of expense.")
    amount: float = Field(gt=0, description="Amount of expense.")
    description: Optional[str] = Field(default="")

    class Config:
        extra = "forbid"  # Disallow extra fields
        json_schema_extra = {
            "example": {
                "date": "2024-08-18",
                "category": "transport",
                "amount": 1000,
                "description": ""
            }
        }

    @field_validator("date")
    def validate_date(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be valid and in format YYYY-MM-DD.")
        return value

    @field_validator("category")
    def validate_category(cls, value):
        categories = ["housing", "transport", "food", "clothing", "other"]
        if value not in categories:
            raise ValueError("Invalid category. Must be one of: housing, transport, food, clothing, other.")
        return value

    @field_validator("amount")
    def validate_amount(cls, value):
        try:
            amount = float(value)
        except ValueError:
            raise ValueError("Amount must be valid integer or float.")
        return value
