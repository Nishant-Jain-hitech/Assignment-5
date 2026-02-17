from typing import List
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


"""Create Models"""


class AuthorModel(BaseModel):
    name: str
    email: EmailStr


class AuthorProfileModel(BaseModel):
    bio: Optional[str]=None



class BlogModel(BaseModel):
    title: str
    content: Optional[str]=None
    published_at: Optional[datetime]=None


class CategoryModel(BaseModel):
    name: str


class BlogCategoryModel(BaseModel):
    blog_id: int
    category_id: int


"""Response Models"""


class AuthorResponseModel(BaseModel):
    id:int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class AuthorProfileResponseModel(BaseModel):
    id:int
    bio: str|None=None
    author_id:int

    class Config:
        from_attributes = True


class BlogResponseModel(BaseModel):
    id:int
    title: str
    content: str|None=None
    author_id:int
    published_at: datetime|None=None

    class Config:
        from_attributes = True


class CategoryResponseModel(BaseModel):
    id:int
    name: str
    
    class Config:
        from_attributes = True


class BlogCategoryResponseModel(BaseModel):
    id:int
    blog_id:int
    category_id:int

    class Config:
        from_attributes = True


class EagerAuthorResponseModel(BaseModel):
    name:str
    profile: str|None=None
    blogs: List[dict]

    class Config:
        from_attributes=True


class EagerBlogResponseModel(BaseModel):
    title:str
    author: str
    categories: List[str]

    class Config:
        from_attributes=True


