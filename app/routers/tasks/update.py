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
from app.schemas import TaskSchema
from app.utils.get import get_task


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/task/update/{task_id}", response_class=HTMLResponse)
async def update_task(request: Request, task_id: int, db: AsyncSession = Depends(get_db)):
    user = await try_get_user(request, db)
    task = await get_task(db=db, id=task_id)
    
    return templates.TemplateResponse("work_space/update_task.html", {"request": request, "user": user, "task": task})



@router.post("/task/update/{task_id}")
async def update_task(
    task_id: int,
    date: TaskSchema,
    db: AsyncSession = Depends(get_db)
):
    task = await get_task(db=db, id=task_id)
    
    due_dt = None
    if date.due_date:
        due_dt = datetime.strptime(date.due_date, "%Y-%m-%dT%H:%M")

    task.title = date.title
    task.description = date.description
    task.due_date = due_dt
    await db.commit()
    return RedirectResponse(url="/dashboard/tasks", status_code=303)