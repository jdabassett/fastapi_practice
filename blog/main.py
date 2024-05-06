from fastapi import FastAPI
from .database import Base, engine
from .routers import blog_router, user_router, authentication_router

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(authentication_router.router)
app.include_router(blog_router.router)
app.include_router(user_router.router)
