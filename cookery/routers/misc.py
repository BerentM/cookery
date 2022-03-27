from fastapi import APIRouter

from ..crud import read

router = APIRouter(
    tags=['misc']
)


@router.get('/')
def index():
    return "Hello World"


@router.get('/about')
def about():
    return read.about()
