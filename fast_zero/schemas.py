from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    ID: int


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    ID: int


class UsersList(BaseModel):
    users: list[UserPublic]
