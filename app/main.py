from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db.database import engine, Base, get_db
from app.main_router import main_router
from fastapi import Request
from fastapi.responses import RedirectResponse
from app.auth.utils import try_get_user



app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(main_router)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.middleware("http")
async def check_auth(request: Request, call_next):
    path = ["/login", "/register", "/static", "/favicon.ico", "/"]

    if request.url.path in path:
        return await call_next(request)
    
    async for db in get_db():
        user = await try_get_user(request, db)
        if not user:
            return RedirectResponse('/')
        break

    response = await call_next(request)
    return response


        