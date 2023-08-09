from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

MAX_POSTS = 100

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# my_posts = [{"title": "title of post 1", "content": "content post 1", "id": 1}, {"title": "title of post 2", "content": "content post 1", "id": 1}]
my_posts = [{"title": f"title of post {i}", "content": f"content post {i}", "id": i} for i in range(1, MAX_POSTS + 1)]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    print(post.rating)
    print(post.model_dump())
    return {"data": post.model_dump()}
    
