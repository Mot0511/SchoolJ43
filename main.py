from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from page_router import page_router
from auth.router import auth_router
from db.engine import create_db

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(auth_router)
app.include_router(page_router)

@app.on_event("startup")
async def startup_event():
    await create_db()