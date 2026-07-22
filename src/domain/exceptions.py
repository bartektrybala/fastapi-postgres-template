import functools
import re
from collections.abc import Callable
from typing import Generic, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def map_specific_exception_regex(
    from_: type[Exception], to: type[Exception], from_message: str, to_message: str
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def wrapper(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def inner(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except from_ as e:
                if re.search(from_message, str(e)):
                    raise to(to_message) from None
                raise e

        return inner

    return wrapper


Model = TypeVar("Model", bound=type[object])


class MissingDbObject(Generic[Model], Exception):
    def __init__(self, model: Model):
        self.model = model
        super().__init__(f"Missing object of type {model.__name__}")


class UserAlreadyExists(Exception):
    pass
