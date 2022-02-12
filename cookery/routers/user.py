from fastapi import APIRouter, status
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

from ..crud import create, delete, read, update
from ..util import schema, auth
from ..util.database import get_db

router = APIRouter(
    prefix="/user",
    tags=['user']
)


@router.get('/{id}', response_model=schema.User)
def get_user(id: int, db: Session = Depends(get_db), current_user: schema.User = Depends(auth.JWT.verify_token)):
    return read.get_user(id, db)

@router.post('/new', status_code=status.HTTP_201_CREATED)
def new_user(request: schema.Login, db: Session = Depends(get_db)):
    return create.add_user(request, db)

@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db), current_user: schema.User = Depends(auth.JWT.verify_token)):
    return delete.delete_user(id, db)

@router.put('/{id}')
def update_user(id: int, request_body: schema.Login, db: Session = Depends(get_db), current_user: schema.User = Depends(auth.JWT.verify_token)):
    return update.update_user(id, request_body, db)