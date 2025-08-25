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


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get('/note/update/{note_id}', response_class=HTMLResponse)
async def edit_note(request: Request, note_id: int, db: AsyncSession = Depends(get_db)):
    user = await try_get_user(request, db)
    note = await get_note(db=db, id=note_id)

    if not note:
        return RedirectResponse(url="/dashboard/note", status_code=404)
    return templates.TemplateResponse("work_space/update_note.html", {"request": request, "user": user, "note": note})


@router.post('/note/update/{note_id}')
async def update_note(
    note_id: int,
    data: NoteSchema,
    db: AsyncSession = Depends(get_db)
):
    note = await get_note(db=db, id=note_id)
    
    if not note:
        return RedirectResponse(url="/dashboard/notes", status_code=404)
    
    note.title = data.title
    note.content = data.content
    await db.commit()
    
    return RedirectResponse(url=f"/note/{note_id}", status_code=303)