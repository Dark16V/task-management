from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request 
from app.models.message import Message
from app.models.task import Task
from app.models.note import Note
import datetime


async def create_note(user_id: int, title: str, content: str, db: AsyncSession = Depends(get_db)):
    note = Note(
        user_id=user_id,
        title=title,
        content=content
    )
    db.add(note)
    await db.commit()


async def create_task(
        user_id: int,
        title: str, 
        description: str = None, 
        from_user_id: int = None, 
        due_date: datetime.datetime = None, 
        visible: bool = True,
        db: AsyncSession = Depends(get_db)
        ):
    
    task = Task(user_id=user_id, 
                title=title, 
                description=description, 
                from_user_id=from_user_id, 
                due_date=due_date, 
                visible=visible
                )
    db.add(task)
    await db.commit()
    return task


async def create_message(receiver_id: int, 
                         title: str, 
                         sender_id: int = None, 
                         task_id: int = None, 
                         db: AsyncSession = Depends(get_db)
                         ):
    message = Message(receiver_id=receiver_id,
                      title=title,
                      sender_id=sender_id,
                      task_id=task_id)
    db.add(message)
    await db.commit()