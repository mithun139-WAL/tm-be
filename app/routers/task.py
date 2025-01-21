from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import async_session
from ..models.task import Task
from ..schemas.task import Task, TaskCreate

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    new_task = Task(**task.dict())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

@router.get("/tasks/", response_model=list[Task])
async def read_tasks(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM tasks LIMIT :limit OFFSET :skip", {"limit": limit, "skip": skip})
    return result.fetchall()
