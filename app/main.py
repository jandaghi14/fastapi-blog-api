from fastapi import FastAPI
from app.routers.router_auth import router_auth
from app.routers.router_post import router_post
app = FastAPI()
app.include_router(router=router_auth)
app.include_router(router=router_post)
