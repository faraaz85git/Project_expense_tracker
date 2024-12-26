from fastapi import APIRouter, HTTPException, Request
from starlette import status
from business_layer.Admin import Admin
from request_response_models.UserResponse import UserResponse


router = APIRouter(tags=["Admin"])


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(request: Request):
    """
        Retrieves a list of all users from the system. Accessible only by an admin user.

        Args:
            request (Request): The FastAPI request object, used to access the current admin's information and logger.

        Returns:
            A list of `UserResponse` objects, each representing a user with their ID, username, and role.

        Raises:
            HTTPException: 500 if any internal server error occurs.
        """

    try:
        admin = Admin(
            username=request.state.user["user_name"],
            role=request.state.user["role"],
            logger=request.state.logger,
        )
        users = admin.show_all_user1()
        result = [
            UserResponse(user_id=user[0], username=user[1], role=user[2])
            for user in users
        ]
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )


@router.get("/users/expenses", status_code=status.HTTP_200_OK)
async def get_users_expenses(request: Request):
    """
        Retrieves the expenses of all users from the system. Accessible only by an admin user.

        Args:
            request (Request): The FastAPI request object, used to access the current admin's information and logger.

        Returns:
            A list of dictionaries, each containing details about a user's expense such as ID, username, date, category, amount, and description.

        Raises:
            HTTPException: 500 if any internal server error occurs.
        """
    try:
        admin = Admin(
            username=request.state.user["user_name"],
            role=request.state.user["role"],
            logger=request.state.logger,
        )
        expenses = admin.show_all_users_expenses1()
        result = [
            {
                "exp_id": expense[0],
                "username": expense[1],
                "date": expense[2],
                "category": expense[3],
                "amount": expense[4],
                "description": expense[5],
            }
            for expense in expenses
        ]

        return result
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )
