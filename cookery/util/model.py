from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import LargeBinary

from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

    recipe = relationship("Recipe", back_populates="user")

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    difficulty = Column(Integer)
    image = Column(LargeBinary)

    user = relationship("User", back_populates="recipe", lazy="subquery")
    description = relationship("Description", back_populates="recipe", lazy="subquery")
    ingredients = relationship("Ingredient", back_populates="recipe", lazy="subquery")

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), index=True)
    name = Column(String)
    quantity = Column(String)

    recipe = relationship("Recipe", back_populates="ingredients")

class Description(Base):
    __tablename__ = "descriptions"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), index=True)
    order = Column(Integer)
    name = Column(String)

    recipe = relationship("Recipe", back_populates="description")
