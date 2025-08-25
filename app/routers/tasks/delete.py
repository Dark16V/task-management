from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from fastapi import HTTPException
from app.utils.get import get_task


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post('/task/delete/{task_id}', response_class=HTMLResponse)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    task = await get_task(db=db, id=task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or you do not have permission to delete it.")
    
    await db.delete(task)
    await db.commit()
    
    return RedirectResponse(url="/dashboard/tasks", status_code=303)