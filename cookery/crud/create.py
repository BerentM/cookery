# TODO: change to classes
from fastapi import HTTPException, status
from starlette.responses import Response
from cookery.util import model, auth, schema


def add_recipe(request_body, db):
    if db.query(model.Recipe).filter(model.Recipe.name == request_body.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"recipe {request_body.name=} already exists"
        )
    recipe = model.Recipe(name=request_body.name, user_id=request_body.user_id,
                          difficulty=request_body.difficulty)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    for item in request_body.description:
        description = model.Description(
            order=item.order,
            description=item.description,
            recipe_id=recipe.id
        )
        db.add(description)

    for item in request_body.ingredients:
        ingredients = model.Ingredient(
            name=item.name,
            quantity=item.quantity,
            recipe_id=recipe.id
        )
        db.add(ingredients)

    db.commit()
    return Response(
        content="sucessfuly added new recipe",
        status_code=status.HTTP_201_CREATED
    )


def add_user(request_body, db) -> schema.Sucess:
    hashed_password = auth.Hash.hash_password(request_body.password)
    if db.query(model.User).filter(model.User.username == request_body.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"user {request_body.username=} already exists"
        )
    new_user = model.User(username=request_body.username,
                          password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return schema.Sucess(
        info=f"Created {new_user.id=}",
        status_code=status.HTTP_201_CREATED
    )
