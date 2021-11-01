from fastapi import FastAPI

from cookery.util import database, model
from cookery.routers import recipes, misc, auth, user

api = FastAPI()
api.include_router(recipes.router)
api.include_router(misc.router)
api.include_router(auth.router)
api.include_router(user.router)

model.Base.metadata.create_all(bind=database.engine)

if __name__ == "__main__":
    print("Wrong file?!?")
