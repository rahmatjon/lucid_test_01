from fastapi import Depends, HTTPException
from app.repositories.post_repository import PostRepository
from app.models.database import SessionLocal
from app.services.auth_service import get_current_user
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PostService:
    def __init__(self, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
        self.db = db
        self.current_user = current_user
        self.post_repo = PostRepository(db)

    def create_post(self, post_data):
        return self.post_repo.create_post(post_data, self.current_user.id)

    def get_user_posts(self):
        return self.post_repo.get_posts(self.current_user.id)

    def delete_post(self, post_id: int):
        if not self.post_repo.delete_post(post_id, self.current_user.id):
            raise HTTPException(status_code=404, detail="Post not found")
        return {"message": "Post deleted successfully"}