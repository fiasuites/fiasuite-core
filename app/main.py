import time
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from requests import Request

# Routers
from app.api.routers import users_routers, auth_routers

app = FastAPI(title="FiaSuite Backend API", version="1.0.0")
app.include_router(auth_routers.router)
app.include_router(users_routers.router)

origins = ["http://localhost", "http://localhost:8080", ""]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_origin_regex="https://.*\.regnify\.com",
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middlewares
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.
    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


use_route_names_as_operation_ids(app)

