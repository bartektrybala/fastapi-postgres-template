import typing as t

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.containers import Container, get_container
from src.domain.auth.exceptions import CurrentUserInvalidCredentials
from src.domain.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: t.Annotated[str, Depends(oauth2_scheme)],
    container: t.Annotated[Container, Depends(get_container)],
) -> User:
    try:
        current_user = container.request_user_service().get_current_user(token=token)
    except CurrentUserInvalidCredentials:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
