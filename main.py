from fastapi import FastAPI,Path,Query
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from Router import Auth,expense,Budget
from starlette import status


app=FastAPI()
app.include_router(Auth.router)
app.include_router(expense.router)
app.include_router(Budget.router)
@app.get("/status",status_code=status.HTTP_200_OK)
async def check_status():
    return {"status":"up"}