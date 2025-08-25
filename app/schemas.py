from pydantic import BaseModel


class NoteSchema(BaseModel):
    title: str
    content: str


class TaskSchema(BaseModel):
    title: str
    description: str
    due_date: str | None = None 



class CreateTaskForFriendSchema(BaseModel):
    username: str
    title: str
    description: str
    due_date: str | None = None