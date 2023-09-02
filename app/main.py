import time
from typing import Optional
from fastapi import FastAPI, Response, status,  HTTPException, Depends
from pydantic import BaseModel
from random import randrange
# from psycopg2 import connect
from psycopg import connect
from psycopg.rows import dict_row
from sqlalchemy.orm import Session

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    
    return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM public." posts" """) # This select format was taken from the pgAdmin when execute a search on the table.
    # posts = cursor.fetchall()
    # print(posts)
    
    posts = db.query(models.Post).all()
    
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # Insert in database with the data already sanited.
    cursor.execute(""" INSERT INTO public." posts" (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    
    return {"data": new_post}
    
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM public." posts" WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with the id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id: {id} was not found")
        
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute(""" DELETE FROM public." posts" WHERE id = %s returning * """, [str(id)])
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute(""" UPDATE public." posts" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
    
    return {"data": updated_post}