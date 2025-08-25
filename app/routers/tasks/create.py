from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.auth.utils import try_get_user
from datetime import datetime
from datetime import datetime
from app.schemas import TaskSchema, CreateTaskForFriendSchema
from app.utils.get import get_task, get_user
from app.utils.create import create_task as crt_task, create_message



router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/task/create", response_class=HTMLResponse)
async def add_task(request: Request, db: AsyncSession = Depends(get_db)):
    user = await try_get_user(request, db)

    return templates.TemplateResponse("work_space/create_task.html", {"request": request, "user": user})


@router.post("/task/create")
async def create_task(
    data: TaskSchema,
    db: AsyncSession = Depends(get_db),
    request: Request = None
):
    user = await try_get_user(request, db)
    due_dt = None
    if data.due_date:  
        due_dt = datetime.strptime(data.due_date, "%Y-%m-%dT%H:%M")

    await crt_task(db=db, user_id=user.id, title=data.title, description=data.description, due_date=due_dt)

    return RedirectResponse(url="/dashboard/tasks", status_code=303)



@router.post('/task/complete/{task_id}', response_class=HTMLResponse)
async def complete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    task = await get_task(db=db, id=task_id)
    
    task.completed = True
    await db.commit()
    
    return RedirectResponse(url="/dashboard/tasks", status_code=303)


@router.get("/task/view/{task_id}", response_class=HTMLResponse)
async def view_task(
    request: Request,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    now: datetime = datetime.utcnow()
):
    user = await try_get_user(request, db)
    task = await get_task(db=db, id=task_id)
    
    return templates.TemplateResponse("work_space/view_task.html", {"request": request, "user": user, "task": task, "now": now})



@router.get('/task/for_friend/', response_class=HTMLResponse)
async def create_task_for_friend(request: Request, db: AsyncSession = Depends(get_db)):
    user = await try_get_user(request, db)
    
    return templates.TemplateResponse("work_space/create_task_for_friend.html", {"request": request, "user": user})



@router.post('/task/for_friend/')
async def add_task_for_friend(
    data: CreateTaskForFriendSchema,
    db: AsyncSession = Depends(get_db),
    request: Request = None):

    user = await try_get_user(request, db)
    friend = await get_user(db=db, username=data.username)

    due_dt = None
    if data.due_date:  
        due_dt = datetime.strptime(data.due_date, "%Y-%m-%dT%H:%M")

    new_task = await crt_task(db=db, 
                                 user_id=user.id, 
                                 from_user_id=friend.id, 
                                 title=data.title, 
                                 description=data.description, 
                                 due_date=due_dt, 
                                 visible=False)

    await db.refresh(new_task)
    await create_message(db=db, 
                         sender_id=user.id, 
                         receiver_id=friend.id, 
                         title=f"{data.username} wants to give you a task:{data.title}", 
                         task_id=new_task.id)
    
    return RedirectResponse(url="/dashboard/tasks", status_code=303)