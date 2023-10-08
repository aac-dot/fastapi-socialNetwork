from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, Response, APIRouter
from typing import List

from ..schemas import PostCreate, Post
from ..database import get_db
from .. import models
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM public." posts" """) # This select format was taken from the pgAdmin when execute a search on the table.
    # posts = cursor.fetchall()
    # print(posts)
    
    posts = db.query(models.Post).all()
    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    # Insert in database with the data already sanited.
    # cursor.execute(""" INSERT INTO public." posts" (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(user_id)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post
    
@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM public." posts" WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with the id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id: {id} was not found")
    
    print(post)
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/{id}", response_model=Post)
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
    
    return post_query.first()
