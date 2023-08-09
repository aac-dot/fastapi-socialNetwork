from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "this is your post"}

@app.post("/posts")
def create_posts(post: Post):
    print(post.rating)
    # return {"new_post": f"title: {new_post['title']} content: {new_post['content']}"}
    # return {"title": payload["title"], "content": payload["content"]}
    print(post.model_dump())
    return {"data": post.model_dump()}
    
