from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import Recipe, Ingredient, RecipeLike, recipe_ingredient
from ..schemas import RecipeCreate, RecipeCreateResponse, IngredientCreate, AdminSchema
from ..database import Base
from ..utils.auth_handler import check_user, signJWT, decodeJWT, token_response
from ..utils.auth_bearer import JWTBearer


router = APIRouter(prefix="/api/v1")

security = HTTPBasic()


@router.post("/admin/login", status_code=status.HTTP_200_OK)
def admin_login(admin: AdminSchema):
    if check_user(admin):
        return signJWT(admin.login)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")



@router.get("/admin/recipes", status_code=status.HTTP_200_OK)
def check_recipe(db: Session = Depends(Base.get_db), token: str = Depends(JWTBearer())):
    recipes = db.query(Recipe).all()
    return recipes



@router.post("/admin/recipe", status_code=status.HTTP_201_CREATED)
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


@router.put("/admin/recipe/{recipe_id}", status_code=status.HTTP_200_OK)
def update_recipe(recipe_id: int, recipe: RecipeCreate, db: Session = Depends(Base.get_db)):
    db.query(Recipe).filter(Recipe.id == recipe_id).delete()
    db.query(recipe_ingredient).filter(recipe_id == recipe_id).delete()
    for ingredient in recipe.ingredients:
        db.query(Ingredient).filter(Ingredient.name == ingredient.name, Ingredient.unit == ingredient.unit).delete()
    db.commit()
    create_recipe(recipe, db)
    return "Updated"
# СТРАННЫЙ БАГ, МЕШАЮТСЯ АЙДИШНИКИ, НАДО ПЕРЕСМОТРЕТЬ СПОСОБ ОБНОВЛЕНИЯ

