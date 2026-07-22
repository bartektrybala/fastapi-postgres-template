import typing as t
from typing import Literal, TypedDict

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import text

from src.containers import Container, get_container

router = APIRouter()


class StatusOK(TypedDict):
    status: Literal["ok"]


@router.get("/health")
async def health(container: t.Annotated[Container, Depends(get_container)]) -> StatusOK:
    session = container.session()
    result = session.execute(text("SELECT 1"))
    assert result.scalar() == 1, "Database connection failed"
    return {"status": "ok"}
