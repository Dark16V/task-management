from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.models.message import Message
from app.models.task import Task
from app.models.note import Note


async def delete_object(object: Task | Message | Note, db: AsyncSession = Depends(get_db)):
    await db.delete(object)
    await db.commit()