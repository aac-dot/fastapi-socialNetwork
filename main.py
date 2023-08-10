from typing import Optional
from fastapi import FastAPI, Response, status,  HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

MAX_POSTS = 100

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# my_posts = [{"title": "title of post 1", "content": "content post 1", "id": 1}, {"title": "title of post 2", "content": "content post 1", "id": 1}]
my_posts = [{"title": f"title of post {i}", "content": f"content post {i}", "id": i} for i in range(1, MAX_POSTS + 1)]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    new_post = post.model_dump() # Convert to dict
    new_post['id'] = randrange(0, 100000)
    my_posts.append(new_post)
    
    return {"data": new_post}
    
@app.get("/posts/{id}")
def get_post(id: int):
    
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with the id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id: {id} was not found")
        
    return {"data": post}