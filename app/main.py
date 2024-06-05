from fastapi import FastAPI
from .database import engine
from . import models
from .routers import auth, posts, users, vote
from fastapi.middleware.cors import CORSMiddleware


'''
We used the below code to tell SQLAlchemy to create the tables from models.py.
SQLAlchemy will create the tables only if there is not any other same table-name already
in the database regardless of your changes in models.py then we had to delete the whole table
then SQLAlchemy would create the table which is unacceptable in production environment
but now we can use "Alembic" library for database migration.
'''
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "hello World"}


