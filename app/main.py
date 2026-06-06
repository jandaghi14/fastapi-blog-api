from fastapi import FastAPI
from app.routers.router_auth import router_auth
from app.routers.router_post import router_post
from app.routers.router_comment import router_comment
from app.routers.router_tag import router_tag
app = FastAPI()
app.include_router(router=router_auth)
app.include_router(router=router_post)
app.include_router(router=router_comment)
app.include_router(router=router_tag)
