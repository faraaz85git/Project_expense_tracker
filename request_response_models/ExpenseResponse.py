from pydantic import BaseModel
class ExpenseResponse(BaseModel):
    exp_id:int
    date: str
    category: str
    amount: float
    description: str

    model_config = {
        "json_schema_extra":{
            "example":{
                    "exp_id": 10,
                    "date": "2024-08-18",
                    "category": "transport",
                    "amount": 1000,
                    "description": ""
            }
        }
    }