"""
Main application module.

This module serves as the entry point of the FastAPI application.
It is responsible for:

- Initializing the FastAPI app instance.
- Managing application lifecycle events (startup and shutdown).
- Registering API routers.
- Mounting static files for frontend delivery.

The application uses a lifespan context manager to initialize shared
resources such as the WordService, which depends on an asynchronous
HTTP client.
"""
import httpx
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.staticfiles import StaticFiles

from app.routers.game import router
from app.services.word_service import WordService



@asynccontextmanager
async def my_lifespan(app):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        app.state.word_service = WordService(client=client)
        yield


app = FastAPI(lifespan=my_lifespan)
app.include_router(router=router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
