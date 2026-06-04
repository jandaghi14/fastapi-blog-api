from fastapi import FastAPI
from app.routers.auth import router_auth

app = FastAPI()
app.include_router(router=router_auth)
