from fastapi import FastAPI
from app.controllers import auth_controller, post_controller
from app.models.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(auth_controller.router)
app.include_router(post_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI MVC App"}