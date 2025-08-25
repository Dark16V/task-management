from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request 
from app.models.message import Message
from app.models.task import Task
from app.models.note import Note
import datetime


async def note_update(note: Note, 
                      user_id: int = None, 
                      title: str = None, 
                      content: str = None, 
                      db: AsyncSession = Depends(get_db)):
    
    note.user_id = user_id if user_id else note.user_id
    note.title = title if title else note.title
    note.content = content if content else note.content
    await db.commit()


async def task_update(task: Task, 
                      user_id: int = None, 
                      from_user_id: int = None, 
                      title: str = None, 
                      description: str = None, 
                      due_date: datetime.datetime = None, 
                      completed: bool = None, 
                      visible: bool = None,
                      db: AsyncSession = Depends(get_db)):
    
    task.user_id = user_id if user_id else task.user_id
    task.from_user_id = from_user_id if from_user_id else task.from_user_id   
    task.title = title if title else task.title
    task.description = description if description else task.description
    task.due_date = due_date if due_date else task.due_date
    task.completed = completed if completed else task.completed
    task.visible = visible if visible else task.visible
    await db.commit()