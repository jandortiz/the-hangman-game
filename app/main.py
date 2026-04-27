
import httpx
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.services.word_service import WordService
from app.routers.game import router
from starlette.staticfiles import StaticFiles


@asynccontextmanager
async def my_lifespan(app):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        app.state.word_service = WordService(client=client)
        yield


app = FastAPI(lifespan=my_lifespan)
app.include_router(router=router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


