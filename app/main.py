import time
from typing import Optional
from fastapi import FastAPI, Response, status,  HTTPException
from pydantic import BaseModel
from random import randrange
# from psycopg2 import connect
from psycopg import connect
from psycopg2.extras import RealDictCursor

MAX_POSTS = 100

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
        conn = connect(conninfo="host=localhost dbname=fastapi user=postgres password=postgres")
        cursor = conn.cursor()
        print(conn)
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connection with database failed")
        print("The following error has happened:", error)
        time.sleep(2)

# my_posts = [{"title": "title of post 1", "content": "content post 1", "id": 1}, {"title": "title of post 2", "content": "content post 1", "id": 1}]
my_posts = [{"title": f"title of post {i}", "content": f"content post {i}", "id": i} for i in range(1, MAX_POSTS + 1)]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM public." posts" """) # This select format was taken from the pgAdmin when execute a search on the table.
    posts = cursor.fetchall()
    
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    new_post = post.model_dump() # Convert to dict
    new_post['id'] = randrange(0, MAX_POSTS)
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

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
    
    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    index = find_index_post(id)
    
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
    
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[id] = post_dict
    
    return {"data": post_dict}