from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.auth.utils import try_get_user
from app.models.task import Task
from sqlalchemy.future import select
from app.models.message import Message


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")




@router.get('/view/message/{msg_id}', response_class=HTMLResponse)
async def view_message(msg_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    user = await try_get_user(request, db)
    message = await db.execute(
        select(Message).where(Message.id == msg_id, Message.receiver_id == user.id)
    )
    message = message.scalar_one_or_none()
    
    
    
    return templates.TemplateResponse("work_space/show_message.html", {"request": request, "message": message})


@router.post('/delete/message/{message_id}')
async def reject_message(message_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    user = await try_get_user(request, db)
    message = await db.execute(
        select(Message).where(Message.id == message_id, Message.receiver_id == user.id)
    )
    message = message.scalar_one_or_none()
    
    await db.delete(message)
    await db.commit()
    
    return RedirectResponse(url="/dashboard/tasks", status_code=303)



@router.post('/accept/message/{message_id}')
async def accept_message(message_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    message = await db.execute(
        select(Message).where(Message.id == message_id)
    )
    message = message.scalar_one_or_none()
    
    task = await db.execute(
        select(Task).where(Task.id == message.task_id)
    )
    task = task.scalar_one_or_none()
    task.visible = True
    await db.delete(message)
    await db.commit()

    
    return RedirectResponse(url="/dashboard/tasks", status_code=303)