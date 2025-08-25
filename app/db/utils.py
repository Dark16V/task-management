from app.db.database import get_db
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request 
from app.models.message import Message
from app.models.task import Task
from app.models.note import Note
from app.models.users import User



async def get_message(id: int = None, sender: int = None, receiver: int = None, db: AsyncSession = Depends(get_db)):
    if id:
        message = await db.execute(select(Message).where(Message.id == id))
        return message.scalar_one_or_none()
    if sender:
        message = await db.execute(select(Message).where(Message.sender_id == sender))
        return message.scalars().all()
    if receiver:
        message = await db.execute(select(Message).where(Message.receiver_id == receiver))
        return message.scalars().all()


async def get_task(id: int = None, user_id: int = None, from_user_id: int = None, visible: bool = True, db: AsyncSession = Depends(get_db)):
    if id:
        task = await db.execute(select(Task).where(Task.id == id))
        return task.scalar_one_or_none()  
    task = select(Task)
    if user_id:
        task = task.where(Task.user_id == user_id)

    if from_user_id:
        task = task.where(Task.from_user_id == from_user_id)

    if visible:
        task = task.where(Task.visible == visible)
    result = await db.execute(task)
    return result.scalars().all()



async def get_note(id: int = None, user_id: int = None, db: AsyncSession = Depends(get_db)):
    if id:
        note = await db.execute(select(Note).where(Note.id == id))
        return note.scalar_one_or_none()  
    if user_id:
        note = await db.execute(select(Note).where(Note.user_id == user_id))
        return note.scalars().all()
    

async def get_user(id: int = None, username: str = None, db: AsyncSession = Depends(get_db)):
    if id:
        user = await db.execute(select(User).where(User.id==id))
        return user.scalar_one_or_none()
    if username:
        user = await db.execute(select(User).where(User.username == username))
        return user.scalar_one_or_none()
