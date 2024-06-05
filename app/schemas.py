from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:  # this is mandatory only for response of API. maybe cause of SQLAlchemy IDK.
        # orm_mode = True
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut 

    class Config:
        # orm_mode = True
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:  
        # orm_mode = True
        from_attributes = True



class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    # id: Optional[str] = None # 'same as tutorial but raised error for me'


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)] # It accepts only 0 or 1

