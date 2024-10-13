from pydantic import field_validator, BaseModel,Field
from datetime import datetime

class BudgetCreate(BaseModel):
    housing:float=Field(gt=0,description="Budget for housing.")
    transport:float=Field(gt=0,description="Budget for housing.")
    food:float=Field(gt=0,description="Budget for food.")
    clothing:float=Field(gt=0,description="Budget for clothing.")
    other:float=Field(gt=0,description="Budget for other.")
    start_date:str=Field(description="Start date of budget.")
    end_date:str=Field(description="End date of budget.")

    class Config:
        extra="forbid"
        json_schema_extra={
            "example":{
                "housing":1200.0,
                "transport": 1200.0,
                "food": 1200.0,
                "clothing": 1200.0,
                "other": 1200.0,
                "start_date":"2024-12-12",
                "end_date": "2024-12-12"
            }
        }

    @field_validator("start_date")
    def validate_start_date(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be valid and in format YYYY-MM-DD.")
        return value

    @field_validator("end_date")
    def validate_end_date(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be valid and in format YYYY-MM-DD.")
        return value
