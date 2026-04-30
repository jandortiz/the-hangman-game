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
    """Manages application startup and shutdown lifecycle.

    This context manager is executed when the application starts and stops.
    It initializes shared resources and attaches them to the application state.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Control is yielded back to the application runtime.

    Behavior:
        - Creates a reusable asynchronous HTTP client.
        - Instantiates the WordService with the HTTP client.
        - Stores the WordService in `app.state` for global access.
        - Ensures proper cleanup of the HTTP client on shutdown.

    Notes:
        - `app.state.word_service` can be accessed in route handlers
          via the Request object.
        - The HTTP client is automatically closed when the application stops.
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        app.state.word_service = WordService(client=client)
        yield


app = FastAPI(lifespan=my_lifespan)
app.include_router(router=router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
