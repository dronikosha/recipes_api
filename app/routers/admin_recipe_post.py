from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.models.models import Recipe, Ingredient, RecipeLike, recipe_ingredient
from ..schemas import RecipeCreate, RecipeCreateResponse, IngredientCreate
from ..database import Base

router = APIRouter()


@router.post("/recipe", status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(Base.get_db)):
    db_recipe = Recipe(
        name=recipe.name,
        description=recipe.description,
        photo_url=recipe.photo_url,
        instructions=recipe.instructions
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    for ingredient in recipe.ingredients:
        db_ingredient = Ingredient(
            name=ingredient.name,
            unit=ingredient.unit
        )
        db.add(db_ingredient)
        db.commit()
        db.refresh(db_ingredient)

        db_recipe_ingredient = recipe_ingredient.insert().values(
            recipe_id=db_recipe.id,
            ingredient_id=db_ingredient.id,
            amount=ingredient.amount
        )
        db.execute(db_recipe_ingredient)
    db.refresh(db_recipe)

    return "Created recipe"
