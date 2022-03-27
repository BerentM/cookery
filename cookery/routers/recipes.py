from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session
from starlette.responses import Response

from ..crud import create, delete, read, update
from ..util import auth, schema
from ..util.database import get_db

router = APIRouter(
    prefix='/recipe',
    tags=['recipe']
)


@router.get('/all')
def recipes_list(
        id_from: int = 0,
        id_to: int = 10,
        db: Session = Depends(get_db),
        current_user: schema.User = Depends(auth.JWT.verify_token)):
    return read.recipe_list(id_from, id_to, db)


@router.get('/list')
def recipes_simple_list(
        db: Session = Depends(get_db),
        current_user: schema.User = Depends(auth.JWT.verify_token)):
    return read.recipe_simple_list(db)


@router.post('/new', status_code=status.HTTP_201_CREATED)
async def add_recipe(recipe: schema.New_Recipe,
                     db: Session = Depends(get_db),
                     current_user: schema.User = Depends(auth.JWT.verify_token)):
    return create.add_recipe(recipe, db)


@router.get('/{id}', response_model=schema.Recipe)
def read_single_recipe(id: int,
                       db: Session = Depends(get_db),
                       current_user: schema.User = Depends(auth.JWT.verify_token)):
    return read.single_recipe(id, db)


@router.put('/{id}')
def update_recipe(id: int,
                  recipe: schema.New_Recipe,
                  db: Session = Depends(get_db),
                  current_user: schema.User = Depends(auth.JWT.verify_token)):
    return update.update_recipe(id, recipe, db)


@router.delete('/{id}', response_class=Response)
def delete_recipe(id: int,
                  db: Session = Depends(get_db),
                  current_user: schema.User = Depends(auth.JWT.verify_token)):
    return delete.delete_recipe(id, db)


@router.get('/{id}/ingredients', response_model=schema.Ingredient_List)
def recipe_ingredients(id: int,
                       db: Session = Depends(get_db),
                       current_user: schema.User = Depends(auth.JWT.verify_token)):
    return read.recipe_ingredients(id, db)


@router.get('/{id}/description', response_model=schema.Description_List)
def recipe_description(id: int,
                       db: Session = Depends(get_db),
                       current_user: schema.User = Depends(auth.JWT.verify_token)):
    return read.recipe_description(id, db)
