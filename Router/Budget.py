from fastapi import APIRouter,status,Path,Query,HTTPException
from Router.expense import user_dependency
from business_layer.Budget import Budget
from custom_exception.custom_exception import SQLiteException,NoRecordFoundException,BudgetNotSetException
from request_response_models.BudgetResponse import BudgetResponse
from request_response_models.BudgetCreate import BudgetCreate
from db_layer.myutils import validate_budget_date

router=APIRouter(
    tags=["Budget"]
)

@router.get("/budget/active_budget",status_code=status.HTTP_200_OK)
def get_active_budget(user:user_dependency):
    try:
        active_budget=Budget().active_budget(user.username)
        if active_budget:
             active_budget=active_budget[0]
             return BudgetResponse(housing=active_budget[0],
                                   transport=active_budget[1],
                                   food=active_budget[2],
                                   clothing=active_budget[3],
                                   other=active_budget[4],
                                   start_date=active_budget[5],
                                   end_date=active_budget[6])

        else:
            raise NoRecordFoundException("No active budget is found.")

    except NoRecordFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=e.message)
    except SQLiteException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail="Internal server error.")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail="Internal server error.")

@router.get("/budget/budget_status",status_code=status.HTTP_200_OK)
async def get_budget_status(user:user_dependency):
    try:
        budget_status=user.show_budget_status_by_category2()
        if budget_status:
            return {
                "start_date":budget_status[3],
                "end_date":budget_status[4],
                "budget_amount":budget_status[0],
                "amount_spend":budget_status[1],
                "budget_status":budget_status[2]
            }
        else:
            raise NoRecordFoundException("No budget to show budget status.")
    except NoRecordFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.message)
    except SQLiteException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error.")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error.")


@router.post("/budget",status_code=status.HTTP_204_NO_CONTENT)
async def set_budget(user:user_dependency,
                     new_budget:BudgetCreate):
    try:
        validate_budget_date(new_budget.start_date,new_budget.end_date)
        new_budget = new_budget.model_dump()
        new_budget.update({"username": user.username})
        print(new_budget)
        user.set_budget_by_category2(new_budget=new_budget)
    except BudgetNotSetException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))



