from pydantic import BaseModel
from typing import List, Optional


class IngredientCreate(BaseModel):
    name: str
    unit: str
    amount: float


class RecipeCreate(BaseModel):
    name: str
    description: str
    photo_url: Optional[str]
    instructions: str
    ingredients: List[IngredientCreate]


class RecipeCreateResponse(BaseModel):
    id: int
    name: str
    description: str
    photo_url: Optional[str]
    instructions: str
    ingredients: List[IngredientCreate]
    
    
class AdminSchema(BaseModel):
    login: str
    password: str
