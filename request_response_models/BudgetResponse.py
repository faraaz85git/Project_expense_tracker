from pydantic import field_validator, BaseModel,Field


class BudgetResponse(BaseModel):
    housing:float=Field(description="Budget for housing.")
    transport:float=Field(description="Budget for housing.")
    food:float=Field(description="Budget for food.")
    clothing:float=Field(description="Budget for clothing.")
    other:float=Field(description="Budget for other.")
    start_date:str=Field(description="Start date of budget.")
    end_date:str=Field(description="End date of budget.")

    class Config:
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
