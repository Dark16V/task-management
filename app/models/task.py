from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from sqlalchemy import ForeignKey, DateTime, String


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    due_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    completed: Mapped[bool] = mapped_column(default=False)
    visible: Mapped[bool] = mapped_column(default=True)

