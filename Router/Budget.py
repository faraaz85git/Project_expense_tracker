from fastapi import APIRouter, status, HTTPException
from Router.expense import user_dependency
from business_layer.Budget import Budget
from custom_exception.custom_exception import (
    SQLiteException,
    NoRecordFoundException,
    BudgetNotSetException,
)
from request_response_models.BudgetResponse import BudgetResponse
from request_response_models.BudgetCreate import BudgetCreate
from db_layer.myutils import validate_budget_date

router = APIRouter(tags=["Budget"])


@router.get("/budget", status_code=status.HTTP_200_OK)
def get_active_budget(user: user_dependency):
    """
        Retrieve the currently active budget for the logged-in user.

        Args:
            user: The current logged-in user (either User or Admin).

        Returns:
             The details of the active budget, or a message indicating no active budget is found.

        Raises:
            HTTPException: 500 if an internal server error occurs or db error.
        """
    try:
        user.logger.log(message="Request is processing.")
        active_budget = Budget(logger=user.logger).active_budget(user.username)
        if active_budget:
            active_budget = active_budget[0]
            user.logger.log(message="Active budget is fetched.")
            return BudgetResponse(
                housing=active_budget[0],
                transport=active_budget[1],
                food=active_budget[2],
                clothing=active_budget[3],
                other=active_budget[4],
                start_date=active_budget[5],
                end_date=active_budget[6],
            )

        else:
            return {"status": "No active budget is found."}
    except SQLiteException:
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


@router.get("/budget/status", status_code=status.HTTP_200_OK)
async def get_budget_status(user: user_dependency):
    """
        Get the status of the currently active or last active budget, including budget amount, amount spent,
        and the remaining amount within the active period.

        Args:
            user: The current logged-in user (either User or Admin).

        Returns:
            A dictionary containing the start date, end date, budget amount, amount spent, and the remaining budget status.
            If no budget is found, a message is returned.

        Raises:
            HTTPException: 500 if an internal server error occurs.
        """

    try:
        user.logger.log(message="Request is processing.")
        budget_status = user.show_budget_status_by_category()
        if budget_status:
            return {
                "start_date": budget_status[3],
                "end_date": budget_status[4],
                "budget_amount": budget_status[0],
                "amount_spend": budget_status[1],
                "budget_status": budget_status[2],
            }
        else:
            return {"status": "No budget to show status."}

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


@router.post("/budget", status_code=status.HTTP_201_CREATED)
async def set_budget(user: user_dependency, new_budget: BudgetCreate):
    """
       Set a new budget for the logged-in user if there is no active budget.

       Args:
           user: The current logged-in user (either User or Admin).
           new_budget: The budget data to be set, including housing, transport, food, clothing, other, start date, and end date.

       Returns:
           A confirmation message indicating the budget has been successfully created.

       Raises:
           HTTPException: 400 if there is an active budget or new_budget is overlapping with prev budget.
           HTTPException: 500 if an internal server error occurs.
       """
    try:
        validate_budget_date(new_budget.start_date, new_budget.end_date)
        new_budget = new_budget.model_dump()
        new_budget.update({"username": user.username})
        user.set_budget_by_category(new_budget=new_budget)
        return {"created": "success"}
    except BudgetNotSetException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )
