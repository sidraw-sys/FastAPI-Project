from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.types import conint

#Base Model for Post which will have to be followed when client side is sending data in the body to API server during creating/updating posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True
    #rating: Optional[int]=None


class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    email : EmailStr
    id : int
    created_at : datetime

    class Config:
        orm_mode = True
        
class PostResponse(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post:PostResponse #after JOIN query, we are getting result from the query (without response model in endpoint) as 2 attributes, Post and votes so we will make this Post attribute validate against our previous PostResponse schema.
    votes:int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str




class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : int
    #email : EmailStr

class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)
