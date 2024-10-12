from fastapi import APIRouter,HTTPException,Path,Query,Depends
from typing import Optional,Annotated,Union,Any
from custom_exception.custom_exception import validate_expense,InvalidDate,InvalidCategory,SQLiteException
from starlette import status
from datetime import datetime
from pydantic import field_validator,Field,BaseModel
from business_layer.user import User
from business_layer.Admin import Admin
from Router.Auth import get_curr_user

class ExpenseCreate(BaseModel):
        date:str=Field(description="Date must be in YYYY-MM-DD format.")
        category:str=Field()
        amount:float=Field(gt=0)
        description:Optional[str]=Field(default="")

        model_config = {
            "json_schema_extra":{
                "example":{
                    "date": "2024-08-18",
                    "category": "transport",
                    "amount": 1000,
                    "description": ""
                }
            }
        }

        @field_validator("date")
        def validate_date(cls,value):
            try:
                datetime.strptime(value,"%Y-%m-%d")
            except ValueError:
                raise ValueError("Date must be valid and in format YYYY-MM-DD.")
            return value
        @field_validator("category")
        def validate_category(cls, value):
                categories=["housing","transport","food","clothing","other"]
                if value not in categories:
                    raise ValueError("Invalid category. Must be one of: housing, transport, food, clothing, other.")
                return value

        @field_validator("amount")
        def validate_amount(cls,value):
            try:
                amount=float(value)
            except ValueError:
                raise ValueError("Amount must be valid integer or float.")
            return value

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
class ExpenseUpdate(BaseModel):
    date: Optional[str]=Field()
    category: Optional[str]
    amount: Optional[float]=Field(gt=0)
    description: Optional[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "date": "2024-08-18",
                "category": "transport",
                "amount": 1000,
                "description": ""
            }
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


router=APIRouter(
    tags=["Expenses"]
)
user_dependency=Annotated[Union[User,Admin],Depends(get_curr_user)]
@router.get("/expenses",status_code=status.HTTP_200_OK,response_model=list[ExpenseResponse])
async def get_all_expense(user:user_dependency):
    print(user)
    if user:
        data=user.show_all_expense2()
        print(data)
        if data:
            result=[]
            for d in data:
                result.append(ExpenseResponse(exp_id=d[0], date=d[1], category=d[2], amount=d[3], description=d[4]))
            return result
        else:
            raise HTTPException(status_code=404,detail="Resource not found.")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid API request. you are not logged in")

@router.post("/expenses",status_code=status.HTTP_204_NO_CONTENT)
async def create_expense(expense:ExpenseCreate,user:user_dependency):
    try:
        user.add_expense1(**expense.model_dump())
    except SQLiteException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error")



@router.patch("/expenses/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_expense(expense:ExpenseUpdate,
                         user:user_dependency,
                         expense_id:int=Path(gt=0)):

        try:
            user.expense.update_expense(expense.model_dump(),expense_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e.message)
        except SQLiteException:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal server error.")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal server error.")


@router.get("/get_user_info",status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency):
    return {"a":user.role,"b":user.password}