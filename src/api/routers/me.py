import typing as t

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.domain import aliases
from src.domain.auth.current_user import get_current_user
from src.domain.models import User

router = APIRouter()


class OutputSchema(BaseModel):
    id: aliases.UserPk
    email: str


@router.get("/user/me")
async def me(
    current_user: t.Annotated[User, Depends(get_current_user)],
) -> OutputSchema:
    return OutputSchema(id=current_user.id, email=current_user.email)
