from pydantic import BaseModel


class UserLoginIn(BaseModel):
    username: str
    password: str


class UserLoginOut(BaseModel):
    access_token: str
    refresh_token: str


class UserRefreshIn(BaseModel):
    refresh_token: str


class UserRefreshOut(BaseModel):
    access_token: str
    refresh_token: str
