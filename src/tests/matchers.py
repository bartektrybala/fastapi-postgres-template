from typing import Union, get_args, get_origin


class _AnyMatcher:
    def __call__(self, type: type) -> object:
        return _TypeMatcher(type)

    def __eq__(self, other: object) -> bool:
        return True


class _TypeMatcher:
    def __init__(self, type: type) -> None:
        self.type = type

    def __eq__(self, other: object) -> bool:
        if get_origin(self.type) == Union:
            return any(isinstance(other, t) for t in get_args(self.type))
        return isinstance(other, self.type)


Any = _AnyMatcher()
