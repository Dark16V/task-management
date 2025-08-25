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
from app.db.utils import get_message, get_task


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")




@router.get('/view/message/{msg_id}', response_class=HTMLResponse)
async def view_message(msg_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    message = await get_message(db=db, id=msg_id)
    return templates.TemplateResponse("work_space/show_message.html", {"request": request, "message": message})


@router.post('/delete/message/{message_id}')
async def reject_message(message_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    user = await try_get_user(request, db)
    message = await get_message(db=db, id=message_id)

    if message.task_id:
        task = await get_task(db=db, id=message.task_id)

        new_message = Message(
            sender_id=message.receiver_id,
            receiver_id=message.sender_id,
            title=f'User {user.username} did not accept your task "{task.title}"'
        )
        db.add(new_message)
        await db.delete(task)
    
    await db.delete(message)
    await db.commit()
    
    return RedirectResponse(url="/dashboard/tasks", status_code=303)



@router.post('/accept/message/{message_id}')
async def accept_message(message_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    user = await try_get_user(request, db)
    message = await get_message(db=db, id=message_id)

    if message.task_id:
        task = await get_task(db=db, id=message.task_id)
        task.visible = True

        new_message = Message(
            sender_id=message.receiver_id,
            receiver_id=message.sender_id,
            title=f"User {user.username} accept your task {task.title}"
        )
        db.add(new_message)

    await db.delete(message)
    await db.commit()

    
    return RedirectResponse(url="/dashboard/tasks", status_code=303)