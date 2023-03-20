from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session, joinedload
from app.models.models import Recipe, Ingredient, RecipeLike, recipe_ingredient
from ..schemas import RecipeCreate, RecipeCreateResponse, IngredientCreate
from ..database import Base

router = APIRouter(prefix="/api/v1")


@router.get("/recipes-ingredients", status_code=status.HTTP_200_OK)
def get_recipes(db: Session = Depends(Base.get_db)):
    recipes = db.query(Recipe).options(joinedload(Recipe.ingredients)).all()
    for recipe in recipes:
        for ingredient in recipe.ingredients:
            amount = db.query(recipe_ingredient.c.amount).filter_by(
                recipe_id=recipe.id, ingredient_id=ingredient.id).scalar()
            ingredient.amount = amount
    return recipes
    
    
@router.get("/recipes/{recipe_id}")
def read_recipe(recipe_id: int, db: Session = Depends(Base.get_db)):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()

@router.get("/recipes")
def read_recipes(db: Session = Depends(Base.get_db)):
    return db.query(Recipe).all()