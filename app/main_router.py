from fastapi import APIRouter
from app.auth.router import router as auth_router
from app.routers.notes.create import router as create_note_router
from app.routers.notes.delete import router as delete_note_router
from app.routers.notes.update import router as update_notes_router
from app.routers.tasks.create import router as create_task_router
from app.routers.tasks.delete import router as delete_task_router
from app.routers.tasks.update import router as update_task_router
from app.routers.work_space import router as home_router
from app.routers.messages import router as messages_router

main_router = APIRouter()

routers = [
    auth_router,
    home_router,
    create_note_router,
    create_task_router,
    delete_note_router,
    update_notes_router,
    delete_task_router,
    update_task_router,
    messages_router
]

for router in routers:
    main_router.include_router(router)
