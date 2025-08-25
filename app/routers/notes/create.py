from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.auth.utils import try_get_user
from app.schemas import NoteSchema
from app.utils.get import get_note
from app.utils.create import create_note


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/note/create", response_class=HTMLResponse)
async def add_note(request: Request, db: AsyncSession = Depends(get_db)):
    user = await try_get_user(request, db)

    return templates.TemplateResponse("work_space/create_note.html", {"request": request, "user": user})


@router.post("/note/create", response_class=HTMLResponse)
async def create_note(
    request: Request,
    data: NoteSchema,
    db: AsyncSession = Depends(get_db)
):
    user = await try_get_user(request, db)
    
    await create_note(db=db, user_id=user.id, title=data.title, content=data.content)
    
    return RedirectResponse(url="/dashboard/notes", status_code=303)


@router.get("/note/{note_id}", response_class=HTMLResponse)
async def view_note(request: Request, note_id: int, db: AsyncSession = Depends(get_db)):
    user = await try_get_user(request, db)
    note = await get_note(db=db, id=note_id)
    
    if not note:
        return RedirectResponse(url="/dashboard/notes", status_code=404)
    
    return templates.TemplateResponse("work_space/view_note.html", {"request": request, "user": user, "note": note})



