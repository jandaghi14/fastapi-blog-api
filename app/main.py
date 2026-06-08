import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.limiter import limiter
from app.core.exceptions import NotFoundException, UnauthorizedException, AlreadyExistsException
from app.core.logger import logger
from app.routers.router_auth import router_auth
from app.routers.router_post import router_post
from app.routers.router_comment import router_comment
from app.routers.router_tag import router_tag

app = FastAPI()

app.state.limiter = limiter


@app.exception_handler(Exception)
async def global_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.detail})


@app.exception_handler(UnauthorizedException)
async def unauthorized_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(status_code=401, content={"detail": exc.detail})


@app.exception_handler(AlreadyExistsException)
async def already_exists_handler(request: Request, exc: AlreadyExistsException):
    return JSONResponse(status_code=400, content={"detail": exc.detail})


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router=router_auth)
app.include_router(router=router_post)
app.include_router(router=router_comment)
app.include_router(router=router_tag)


@app.middleware('http')
async def log_requests(request: Request, call_next):
    star_time = time.time()

    response = await call_next(request)

    process_time = time.time() - star_time

    logger.info(f"{request.method} {request.url.path} --- {process_time:.4f}s")
    return response
c = 1+1
