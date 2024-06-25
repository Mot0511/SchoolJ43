from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from page_router import page_router
from auth.router import auth_router
from db.engine import create_db
import uvicorn

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(auth_router)
app.include_router(page_router)

@app.on_event("startup")
async def startup_event():
    await create_db()

if __name__ == "__main__":
  uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)