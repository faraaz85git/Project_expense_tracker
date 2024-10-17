from fastapi import FastAPI, Path, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from Routes.ProjectRoutes import role_to_routes, private_routes
from logger.Logger import Logger
import time
from starlette.responses import Response
from Router.Auth import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from fastapi import FastAPI, status, HTTPException


def logger_obj(request):
    method = request.method
    path = request.url.path
    client_host = request.client.host
    client_port = request.client.port
    logger = Logger(
        "Logs/logs.log",
        log_name=f"{client_host}:{client_port} {method} {path}",
    )
    return logger


def decode_token(token: str):
    try:
        token = token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user = {"user_name": payload.get("user_name"), "role": payload.get("role")}
        if user.get("user_name") == None or user.get("role") == None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized:Invalid request or token.",
            )
        else:
            return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized:Invalid request or token.",
        )


class RoleBasedAcessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger = logger_obj(request)
        try:
            if request.url.path in private_routes:
                token = request.headers.get("Authorization")
                if token:
                    user = decode_token(token)
                    if user["role"] in role_to_routes.get(request.url.path):
                        logger.log(message="Authorized to access route.")
                        request.state.user = user
                        request.state.logger = logger
                        res = await call_next(request)
                        logger.log(
                            message=f"[Status: {res.status_code}] [Time: {time.time() - start_time}]"
                        )
                        return res
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Forbidden: You do not have permission to access this resource.",
                        )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Unauthorized:Invalid request or token.",
                    )
            else:
                logger.log("Authorized to access route.")
                request.state.logger = logger
                res = await call_next(request)
                logger.log(
                    message=f"[Status: {res.status_code}] [Time: {time.time() - start_time}]"
                )
                return res

        except HTTPException as e:
            logger.log(
                message=f"[Status: {e.status_code}] {e.detail} [Time: {time.time()-start_time}]"
            )
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
