# TODO: change to classes
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from cookery.util import model, schema


def single_recipe(id: int, db: Session) -> schema.Recipe:
    recipe = db.query(model.Recipe).get(id)
    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"recipe {id=} not found"
            )
    return schema.Recipe(
            name=recipe.name,
            id = recipe.id,
            user_id = recipe.user_id,
            difficulty=recipe.difficulty,
            ingredients = recipe.ingredients,
            description = recipe.description
    )

def recipe_ingredients(id: int, db: Session) -> schema.Ingredient_List:
    def parse_ingredient(ingredient):
        return schema.Ingredient(
            quantity = ingredient.quantity,
            name = ingredient.name
            )

    recipe = single_recipe(id, db)
    ingredients = recipe.ingredients

    return schema.Ingredient_List(
        recipe_id = id,
        ingredients =  [parse_ingredient(ingredient) for ingredient in ingredients],
        )

def recipe_description(id: int, db: Session)-> schema.Description_List:
    def parse_description(description):
        return schema.Recipe_Description(
            order = description.order,
            description = description.description
            )

    recipe = single_recipe(id, db)
    descriptions = recipe.description

    return schema.Description_List(
            recipe_id = id,
            description = [parse_description(description) for description in descriptions],
            )


def recipe_list(id_from: int, id_to: int, db: Session) -> list[schema.Recipe]:
    recipes = db.query(model.Recipe).order_by(model.Recipe.id).offset(id_from).limit(id_to).all()
    output = []

    for recipe in recipes:
        output.append({
            "id": recipe.id,
            "name": recipe.name,
            "user_id": recipe.user_id,
            "ingredients": recipe.ingredients,
            "description": recipe.description,
        })
    return output

def recipe_simple_list(db:Session) -> list[schema.Simple_Recipe]:
    recipes = db.query(model.Recipe).order_by(model.Recipe.id).all()
    print(recipes)
    output = []

    for recipe in recipes:
        output.append(
            schema.Simple_Recipe(
                id = recipe.id,
                name = recipe.name,
                difficulty = recipe.difficulty,
                user_id = recipe.user_id,
                )
            )
    return output



def get_user(id: int, db: Session) -> schema.User:
    user = db.query(model.User).get(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"username {id=} not found"
            )
    return schema.User(username=user.username)

def about() -> dict:
    return {
        'purpose': 'Cookery API was created to provide comfortable solution for storing cooking recipes.',
        'usage': 'Look at /docs for endpoints documentation.',
        'tech_stack': 'Love, Python and FastAPI!'
    }
