# TODO: change to classes
from sqlalchemy.orm.session import Session
from cookery.util import model, schema
from fastapi import Response, status, HTTPException


def update_recipe(id: int, request_body: schema.New_Recipe, db: Session):
    if db.query(model.Recipe).filter(model.Recipe.id==id).first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"recipe with {id=} not found"
            )
    db.query(model.Recipe).filter(model.Recipe.id==id).update(
        {
            model.Recipe.name: request_body.name,
            model.Recipe.added_by: request_body.added_by
        }
        ,synchronize_session=False)

    db.query(model.Ingredient).filter(model.Ingredient.recipe_id==id).delete(synchronize_session=False)
    for item in request_body.description:
            description = model.Description(
                order=item.order,
                description=item.description, 
                recipe_id=id
                )
            db.add(description)
    
    db.query(model.Description).filter(model.Description.recipe_id==id).delete(synchronize_session=False)
    for item in request_body.ingredients:
        ingredients = model.Ingredient(
            name=item.name, 
            quantity=item.quantity, 
            recipe_id=id
            )
        db.add(ingredients)

    db.commit()

    return Response(status_code=status.HTTP_202_ACCEPTED)

def update_user(id: int, request_body: schema.Login, db: Session):
    if db.query(model.User).filter(model.User.id==id).first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with {id=} not found"
            )
    if db.query(model.User).filter(model.User.username==request_body.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{request_body.username=} already taken"
            )
    
    db.query(model.User).filter(model.User.id==id).update(
        {
            model.User.username: request_body.username,
            model.User.password: request_body.password,
        }
        ,synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_202_ACCEPTED)