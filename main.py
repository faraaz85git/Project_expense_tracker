from fastapi import FastAPI, Path, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Router import Auth, expense, Budget, Admin
from starlette import status
from Middleware.RoleBasedAcessMiddleWare import RoleBasedAcessMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(RoleBasedAcessMiddleware)
app.include_router(Auth.router)
app.include_router(expense.router)
app.include_router(Budget.router)
app.include_router(Admin.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status", status_code=status.HTTP_200_OK)
async def check_status():
    return {"status": "up"}
