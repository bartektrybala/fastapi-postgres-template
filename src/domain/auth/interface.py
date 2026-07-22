import dataclasses
import datetime

import pydantic


@dataclasses.dataclass
class AccesTokenData:
    email: str


class Token(pydantic.BaseModel):
    access_token: str


class TokenPayload(pydantic.BaseModel):
    exp: datetime.datetime
    email: pydantic.EmailStr
