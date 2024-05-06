from fastapi import FastAPI
from .database import Base, engine
from .routers import blog_router, user_router, authentication_router

# api instance
app = FastAPI()

# link session to existing database or create one
Base.metadata.create_all(engine)

# link to all available routes
app.include_router(authentication_router.router)
app.include_router(blog_router.router)
app.include_router(user_router.router)
