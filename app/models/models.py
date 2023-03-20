from app.database import Base
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    photo_url = Column(String(255))
    ingredients = relationship('Ingredient', secondary='recipe_ingredient')
    likes = relationship('RecipeLike')
    instructions = Column(String(1000), nullable=False)

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(255), nullable=False)
    recipes = relationship('Recipe', secondary='recipe_ingredient')

recipe_ingredient = Table('recipe_ingredient', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id')),
    Column('amount', String(255), nullable=False)
)

class RecipeLike(Base):
    __tablename__ = 'recipe_likes'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    like_ip_address = Column(String(255), nullable=False)
    like = Column(Boolean, nullable=False)
