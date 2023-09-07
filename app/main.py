import time
from typing import Optional
from fastapi import FastAPI, Response, status,  HTTPException, Depends
from random import randrange
# from psycopg2 import connect
from psycopg import connect
from psycopg.rows import dict_row
from sqlalchemy.orm import Session

from . import models
from .schemas import PostCreate
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM public." posts" """) # This select format was taken from the pgAdmin when execute a search on the table.
    # posts = cursor.fetchall()
    # print(posts)
    
    posts = db.query(models.Post).all()
    
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    # Insert in database with the data already sanited.
    # cursor.execute(""" INSERT INTO public." posts" (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"data": new_post}
    
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM public." posts" WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with the id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id: {id} was not found")
        
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute(""" DELETE FROM public." posts" WHERE id = %s returning * """, [str(id)])
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")

    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    
    # cursor.execute(""" UPDATE pub lic." posts" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    return {"data": post_query.first()}