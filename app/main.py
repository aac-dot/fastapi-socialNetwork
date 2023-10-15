from fastapi import FastAPI

# import time
# from psycopg2 import connect
# from psycopg import connect
# from psycopg.rows import dict_row

from . import models
from .database import engine

from .routers import post, user, auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
'''
while True:
    # Interface with database
    try:
        # conn = connect(host="localhost", database="fastapi", user="postgres", password="postgres",
        #                cursor_factory=RealDictCursor)
        conn = connect(conninfo="host=localhost dbname=fastapi user=postgres password=postgres", row_factory=dict_row)
        cursor = conn.cursor()
        print(conn)
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connection with database failed")
        print("The following error has happened:", error)
        time.sleep(2)
'''

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}