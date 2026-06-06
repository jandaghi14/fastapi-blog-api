from fastapi import FastAPI
from app.routers.router_auth import router_auth
from app.routers.router_post import router_post
from app.routers.router_comment import router_comment
app = FastAPI()
app.include_router(router=router_auth)
app.include_router(router=router_post)
app.include_router(router=router_comment)
