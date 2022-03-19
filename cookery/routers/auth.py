from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from cookery.util import model
from cookery.util.schema import Token
from ..util import auth, database

router = APIRouter(
    prefix='/login',
    tags = ['authentication']
)

@router.post('', response_model=Token)
def login(request: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter_by(username = request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid credentials!")

    if user.username != request.username or not auth.Hash.verify(request.password,
            user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail='Invalid credentials!')

    acces_token = auth.JWT.create(
        data={'sub': user.username}
    )

    return {'access_token': acces_token, 'token_type': 'bearer'}
