import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.containers import Container, get_atomic_container
from src.domain.user.enums import City
from src.domain.user.exceptions import UserAlreadyExists
from src.domain.user.interfaces import CreateUserDomainDto

router = APIRouter()


class InputSchema(BaseModel):
    email: str
    password: str
    city: City


class OutputSchema(BaseModel):
    id: uuid.UUID
    email: str
    city: City


@router.post("/register", status_code=201)
async def register(
    data: InputSchema,
    container: Annotated[Container, Depends(get_atomic_container)],
) -> OutputSchema:
    try:
        created_user_id = container.user_service().create_user(
            dto=CreateUserDomainDto(
                email=data.email, city=data.city, plain_password=data.password
            )
        )
    except UserAlreadyExists:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )
    return OutputSchema(id=created_user_id, email=data.email, city=data.city)
