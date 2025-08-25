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
from fastapi import HTTPException



router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post('/task/delete/{task_id}', response_class=HTMLResponse)
async def delete_task(
    request: Request,
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    user = await try_get_user(request, db)
    
    task = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user.id)
    )
    task = task.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or you do not have permission to delete it.")
    
    await db.delete(task)
    await db.commit()
    
    return RedirectResponse(url="/dashboard/tasks", status_code=303)