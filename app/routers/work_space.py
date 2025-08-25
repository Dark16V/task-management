from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.auth.utils import try_get_user
from app.models.note import Note
from app.models.task import Task
from sqlalchemy.future import select
from datetime import datetime
from app.models.message import Message
from sqlalchemy import and_
from app.db.utils import get_message, get_note, get_task


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def root(request: Request, db: AsyncSession = Depends(get_db)):
    user = await try_get_user(request, db)

    if user:
        return RedirectResponse(url="/dashboard/notes") 

    return templates.TemplateResponse("auth/home.html", {"request": request})


@router.get("/dashboard/notes", response_class=HTMLResponse)
async def notes(request: Request, db: AsyncSession = Depends(get_db)):
    user = await try_get_user(request, db)

    message = await get_message(db=db, receiver=user.id)
    notes = await get_note(db=db, user_id=user.id)

    return templates.TemplateResponse("work_space/notes.html",
                                      {"request": request, "user": user, "notes": notes, "messages": message})


@router.get("/dashboard/tasks", response_class=HTMLResponse)
async def tasks(request: Request, db: AsyncSession = Depends(get_db), now = datetime.utcnow()):
    user = await try_get_user(request, db)

    tasks = await get_task(db=db, user_id=user.id, visible=True)
    message = await get_message(db=db, receiver=user.id)

    return templates.TemplateResponse("work_space/tasks.html",
                                      {"request": request, "user": user, 'tasks': tasks, 'now': now, "messages": message})