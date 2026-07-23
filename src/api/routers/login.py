import typing as t

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.containers import Container, get_container
from src.domain.auth.interface import AccesTokenData
from src.domain.exceptions import MissingDbObject

router = APIRouter()


class InputSchema(BaseModel):
    email: str
    password: str


class OutputSchema(BaseModel):
    access_token: str
    token_type: t.Literal["bearer"]


@router.post("/login")
async def login(
    credentials: InputSchema,
    container: t.Annotated[Container, Depends(get_container)],
) -> OutputSchema:
    password_service = container.password_service()

    try:
        user = container.user_repository().get_by_email(email=credentials.email)
    except MissingDbObject:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    is_valid = password_service.verify(
        plain_password=credentials.password,
        hashed_password=user.password_hash,
    )
    if not is_valid:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    jwt_token = container.jwt_service().create_access_token(
        data=AccesTokenData(email=user.email)
    )
    return OutputSchema(access_token=jwt_token.access_token, token_type="bearer")
