from fastapi import APIRouter, HTTPException, Path, Query, Depends
from typing import Annotated, Union
from custom_exception.custom_exception import (
    SQLiteException,
    NoRecordFoundException,
    UpdateException,
    InvalidCategoryException,
)
from starlette import status
from business_layer.user import User
from business_layer.Admin import Admin
from Router.Auth import get_curr_user
from request_response_models.ExpenseCreate import ExpenseCreate
from request_response_models.ExpenseResponse import ExpenseResponse
from request_response_models.ExpenseUpdate import ExpenseUpdate

# class ExpenseCreate(BaseModel):
#         date:str=Field(description="Date must be in YYYY-MM-DD format.")
#         category:str=Field(description="Category of expense.")
#         amount:float=Field(gt=0,description="Amount of expense.")
#         description:Optional[str]=Field(default="")
#
#         class Config:
#             extra = "forbid"  # Disallow extra fields
#             json_schema_extra = {
#                 "example": {
#                     "date": "2024-08-18",
#                     "category": "transport",
#                     "amount": 1000,
#                     "description": ""
#                 }
#             }
#
#         @field_validator("date")
#         def validate_date(cls,value):
#             try:
#                 datetime.strptime(value,"%Y-%m-%d")
#             except ValueError:
#                 raise ValueError("Date must be valid and in format YYYY-MM-DD.")
#             return value
#         @field_validator("category")
#         def validate_category(cls, value):
#                 categories=["housing","transport","food","clothing","other"]
#                 if value not in categories:
#                     raise ValueError("Invalid category. Must be one of: housing, transport, food, clothing, other.")
#                 return value
#
#         @field_validator("amount")
#         def validate_amount(cls,value):
#             try:
#                 amount=float(value)
#             except ValueError:
#                 raise ValueError("Amount must be valid integer or float.")
#             return value
#
# class ExpenseResponse(BaseModel):
#     exp_id:int
#     date: str
#     category: str
#     amount: float
#     description: str
#
#     model_config = {
#         "json_schema_extra":{
#             "example":{
#                     "exp_id": 10,
#                     "date": "2024-08-18",
#                     "category": "transport",
#                     "amount": 1000,
#                     "description": ""
#             }
#         }
#     }
# class ExpenseUpdate(BaseModel):
#     date: Optional[str] = Field(None, description="Date of the expense.")
#     category: Optional[str] = Field(None, description="Category of the expense.")
#     amount: Optional[float] = Field(None, gt=0, description="Amount of the expense.")
#     description: Optional[str] = Field(None, description="Description of the expense.")
#
#     class Config:
#         extra = "forbid"  # Disallow extra fields
#         json_schema_extra = {
#             "example": {
#                 "date": "2024-08-18",
#                 "category": "transport",
#                 "amount": 1000,
#                 "description": ""
#             }
#         }
#
#
#
#     @field_validator("date")
#     def validate_date(cls, value):
#         try:
#             datetime.strptime(value, "%Y-%m-%d")
#         except ValueError:
#             raise ValueError("Date must be valid and in format YYYY-MM-DD.")
#         return value
#
#     @field_validator("category")
#     def validate_category(cls, value):
#         categories = ["housing", "transport", "food", "clothing", "other"]
#         if value not in categories:
#             raise ValueError("Invalid category. Must be one of: housing, transport, food, clothing, other.")
#         return value
#
#     @field_validator("amount")
#     def validate_amount(cls, value):
#         try:
#             amount = float(value)
#         except ValueError:
#             raise ValueError("Amount must be valid integer or float.")
#         return value
#

router = APIRouter(tags=["Expenses"])
user_dependency = Annotated[Union[User, Admin], Depends(get_curr_user)]
valid_category = ["housing", "transport", "food", "clothing", "other"]


# @router.get(
#     "/expenses", status_code=status.HTTP_200_OK, response_model=list[ExpenseResponse]
# )
# async def get_all_expense(user: user_dependency):
#     try:
#         user.logger.log(message="Request is processing")
#         data = user.show_all_expense2()
#         result = []
#         for d in data:
#             result.append(
#                 ExpenseResponse(
#                     exp_id=d[0], date=d[1], category=d[2], amount=d[3], description=d[4]
#                 )
#             )
#         return result
#     except SQLiteException as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Internal server error.",
#         )
#     except Exception as e:
#         user.logger.log(message=str(e), level="error")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Internal server error.",
#         )
@router.get("/expenses", status_code=status.HTTP_200_OK)
async def get_expense_by_category(
    user: user_dependency, categories: list[str] = Query(default=[])
):
    """
        Fetch expenses based on provided categories. If no categories are provided,
        it will return all expenses for the current user.

        Args:
            user: The current logged-in user (either User or Admin).
            categories: A list of expense categories to filter by (e.g. "housing", "food", etc.) through query parameter.

        Returns:
            A list of expenses that match the given categories or all expenses if no category is provided.

        Raises:
            HTTPException: 400 if invalid categories are provided.
            HTTPException: 500 if an internal server error occurs or database error.
        """

    try:
        user.logger.log(message="Request is processing.")
        if not categories:
            user.logger.log(message="No category is provided. Fetching all category.")
            expenses = user.show_all_expense()
            result = []
            for expense in expenses:
                result.append(
                    ExpenseResponse(
                        exp_id=expense[0],
                        date=expense[1],
                        category=expense[2],
                        amount=expense[3],
                        description=expense[4],
                    )
                )
            return result
        else:
            categories = [
                category for category in categories if category in valid_category
            ]
            if categories:
                user.logger.log(
                    message="Valid category is provided. Fetching category-wise data."
                )
                expenses = user.show_expense_by_category(categories)
                result = []
                for expense in expenses:
                    result.append(
                        ExpenseResponse(
                            exp_id=expense[0],
                            date=expense[1],
                            category=expense[2],
                            amount=expense[3],
                            description=expense[4],
                        )
                    )
                return result
            else:
                raise InvalidCategoryException()

    except InvalidCategoryException as e:
        user.logger.log(message="Invalid category is provided.", level="error")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except SQLiteException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message
        )
    except Exception as e:
        user.logger.log(message=str(e), level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )

@router.get("/expense", status_code=status.HTTP_200_OK)
async def get_expense_by_category_pagination(
    user: user_dependency, categories: list[str] = Query(default=[]),limit:int =Query(default=10),offset:int=Query(default=0)
):
    """
        Fetch expenses based on provided categories. If no categories are provided,
        it will return all expenses for the current user.

        Args:
            user: The current logged-in user (either User or Admin).
            categories: A list of expense categories to filter by (e.g. "housing", "food", etc.) through query parameter.

        Returns:
            A list of expenses that match the given categories or all expenses if no category is provided.

        Raises:
            HTTPException: 400 if invalid categories are provided.
            HTTPException: 500 if an internal server error occurs or database error.
        """

    try:

        if not categories:
            user.logger.log(message="No category is provided. Fetching all category.")
            expenses = user.show_all_expense_pagination(limit=limit,offset=offset)
            result = []
            for expense in expenses:
                result.append(
                    ExpenseResponse(
                        exp_id=expense[0],
                        date=expense[1],
                        category=expense[2],
                        amount=expense[3],
                        description=expense[4],
                    )
                )
            return result
        else:
            categories = [
                category for category in categories if category in valid_category
            ]
            if categories:
                user.logger.log(
                    message="Valid category is provided. Fetching category-wise data."
                )
                expenses = user.show_expense_by_category_pagination(categories,limit=limit,offset=offset)
                result = []
                for expense in expenses:
                    result.append(
                        ExpenseResponse(
                            exp_id=expense[0],
                            date=expense[1],
                            category=expense[2],
                            amount=expense[3],
                            description=expense[4],
                        )
                    )
                return result
            else:
                raise InvalidCategoryException()

    except InvalidCategoryException as e:
        user.logger.log(message="Invalid category is provided.", level="error")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except SQLiteException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message
        )
    except Exception as e:
        user.logger.log(message=str(e), level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )


@router.post("/expense", status_code=status.HTTP_201_CREATED)
async def create_expense(expense: ExpenseCreate, user: user_dependency):
    """
       Create a new expense record for the current user.

       Args:
           expense: The details of the expense to create (e.g., date, category, amount, description) via pydantic model.
           user: The current logged-in user (either User or Admin).

       Returns:
           A confirmation message that the expense was created successfully.

       Raises:
           HTTPException: 500 if an internal server error occurs or database error.
       """
    try:
        user.add_expense(**expense.model_dump())
        user.logger.log(message="Request is processing")
        return {"status": "Expense created successfully."}
    except SQLiteException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )
    except Exception as e:
        user.logger.log(message=str(e), level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.patch("/expense/{expense_id}", status_code=status.HTTP_200_OK)
async def update_expense(
    expense: ExpenseUpdate, user: user_dependency, expense_id: int = Path(gt=0)
):
    """
        Update an existing expense record for the current user.

        Args:
            expense: The fields to update in the expense (e.g., date, category, amount, description).
            user: The current logged-in user (either User or Admin).
            expense_id: The id of the expense to update.

        Returns:
            A confirmation message that the expense was successfully updated.

        Raises:
            HTTPException: 400 if end_date < start_date.
            HTTPException: 404 if no expense is found with the given ID.
            HTTPException: 500 if an internal server error occurs.
        """
    try:
        user.logger.log(message="Request is processing.")
        user.expense.update_expense(
            username=user.username, filters=expense.model_dump(), expense_id=expense_id
        )
        return {"updated": "success"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NoRecordFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except UpdateException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except SQLiteException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        user.logger.log(message=str(e), level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/expense/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(user: user_dependency, expense_id: int = Path(gt=0)):
    """
        Delete an existing expense record for the current user.

        Args:
            user: The current logged-in user (either User or Admin).
            expense_id: The i of the expense to delete.

        Returns:
            No content upon successful deletion.

        Raises:
            HTTPException: 404 if no expense is found with the given ID.
            HTTPException: 500 if an internal server error occurs due to db error .
        """
    try:
        user.logger.log(message="Request is processing.")
        user.delete_expense(expense_id=expense_id)
    except NoRecordFoundException as e:
        user.logger.log(message=f"No record is found with {expense_id}", level="error")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except SQLiteException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )
    except Exception as e:
        user.logger.log(message=str(e), level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )


@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency):
    """
        Get details of the current logged-in user.

        Args:
            user: The current logged-in user (either User or Admin).

        Returns:
            A dictionary containing the username and role of the current user.
        """
    return {"username": user.username, "role": user.role}
