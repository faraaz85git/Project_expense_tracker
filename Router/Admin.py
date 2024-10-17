from fastapi import APIRouter,HTTPException,Request
from starlette import status
from business_layer.Admin import Admin
from request_response_models.ExpenseResponse import ExpenseResponse
from request_response_models.UserResponse import UserResponse



router=APIRouter(
    tags=["Admin"]
)

@router.get("/users",status_code=status.HTTP_200_OK)
async def get_all_users(request:Request):
      try:
          admin=Admin(username=request.state.user["user_name"],role=request.state.user["role"],logger=request.state.logger)
          users=admin.show_all_user1()
          result=[UserResponse(user_id=user[0],username=user[1],role=user[2]) for user in users]
          return result
      except Exception as e:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Internal server error.")

@router.get("/users/expenses",status_code=status.HTTP_200_OK)
async def get_users_expenses(request:Request):
    try:
        admin = Admin(username=request.state.user["user_name"], role=request.state.user["role"],logger=request.state.logger)
        expenses = admin.show_all_users_expenses1()
        result=[{"exp_id":expense[0],
                 "username":expense[1],
                 "date":expense[2],
                 "category":expense[3],
                 "amount":expense[4],
                 "description":expense[5]}
                 for expense in expenses
                ]

        return result
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error.")




