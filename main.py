from fastapi import FastAPI, HTTPException
from routes.todos import todo_router
from routes.auth import auth_router
from database import init_db
from contextlib import asynccontextmanager
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi

security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Booting up db")
    init_db()
    yield
    print("shutting down")


app = FastAPI(lifespan=lifespan)
app.include_router(todo_router, prefix="/todos")
app.include_router(auth_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Todo App",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
