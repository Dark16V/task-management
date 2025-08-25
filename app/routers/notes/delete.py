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
from sqlalchemy.future import select
from app.db.utils import get_note


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post('/note/delete/{note_id}', response_class=HTMLResponse)
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await get_note(db=db, id=note_id)
    
    if not note:
        return RedirectResponse(url="/dashboard/notes", status_code=404)
    
    await db.delete(note)
    await db.commit()
    
    return RedirectResponse(url="/dashboard/notes", status_code=303)