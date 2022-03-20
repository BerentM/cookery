from typing import List, Optional

from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    quantity: str

    class Config:
        orm_mode = True

class Ingredient_List(BaseModel):
    recipe_id: int
    ingredients: List[Ingredient]

class Recipe_Description(BaseModel):
    order: int
    description: str

    class Config:
        orm_mode = True

class Description_List(BaseModel):
    recipe_id: int
    description: List[Recipe_Description]

class New_Recipe(BaseModel):
    name: str
    difficulty: int
    ingredients: List[Ingredient]
    description: List[Recipe_Description]
    user_id: Optional[int]

    class Config:
        orm_mode = True

class Recipe(New_Recipe):
    id: int

    class Config:
        orm_mode = True

class Sucess(BaseModel):
    status_code: int
    info: str

class Login(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int

class TokenData(BaseModel):
    username: Optional[str] = None
