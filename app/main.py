from fastapi import FastAPI
from routes import auth, post, users
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(post.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to my project"}

