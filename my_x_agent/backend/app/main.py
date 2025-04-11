from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from dotenv import load_dotenv
import os

from app.routes.twitter import router as twitter_router
from app.routes.auth import router as auth_router, get_current_user
from app.routes.twitter_analysis import router as twitter_analysis_router
from app.models.user import User

load_dotenv()

app = FastAPI(
    title="My X Agent API",
    description="API for My X Agent - an AI bot to mimic oneself for X",
    version="0.1.0"
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(twitter_router)
app.include_router(auth_router)
app.include_router(twitter_analysis_router)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to My X Agent API",
        "docs": "/docs",
        "version": "0.1.0"
    }

@app.get("/api/protected-example")
async def protected_route(current_user: User = Depends(get_current_user)):
    """
    Example of a protected route that requires authentication
    """
    return {
        "message": f"Hello, {current_user.username}! This is a protected route.",
        "user_id": current_user.id,
        "email": current_user.email
    }
