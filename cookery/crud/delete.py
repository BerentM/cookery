# TODO: change to classes
from fastapi import status
from sqlalchemy.orm import Session
from cookery.util import model
from fastapi import Response, HTTPException


def delete_recipe(id: int, db: Session):
    if db.query(model.Recipe).filter(model.Recipe.id==id).first():
        db.query(model.Recipe).filter(model.Recipe.id==id).delete(synchronize_session=False)
        db.query(model.Ingredient).filter(model.Ingredient.recipe_id==id).delete(synchronize_session=False)
        db.query(model.Description).filter(model.Description.recipe_id==id).delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(detail=f"recipe {id=} not found", status_code=status.HTTP_404_NOT_FOUND)

def delete_user(id: int, db: Session):
    if db.query(model.User).filter(model.User.id==id).first():
        db.query(model.User).filter(model.User.id==id).delete(synchronize_session=False)

        user_recipes = db.query(model.Recipe).filter(model.Recipe.user_id==id).all()
        for recipe in user_recipes:
            db.query(model.Recipe).filter(model.Recipe.id==recipe.id).update(
                {
                    model.Recipe.user_id: -99
                }, synchronize_session=False)
        
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(detail=f"user {id=} not found", status_code=status.HTTP_404_NOT_FOUND)