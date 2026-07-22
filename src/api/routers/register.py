import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from src.containers import Container, get_atomic_container
from src.domain.exceptions import UserAlreadyExists

router = APIRouter()


class InputSchema(BaseModel):
    email: str
    password: str


class OutputSchema(BaseModel):
    id: uuid.UUID
    email: EmailStr


@router.post("/register", status_code=201)
async def register(
    data: InputSchema,
    container: Annotated[Container, Depends(get_atomic_container)],
) -> OutputSchema:
    repo = container.user_repository()

    try:
        created_user_id = repo.create_user(
            email=data.email,
            password=data.password,
        )
    except UserAlreadyExists:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )
    return OutputSchema(id=created_user_id, email=data.email)
