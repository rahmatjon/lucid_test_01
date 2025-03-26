from sqlalchemy.orm import Session
from app.models.post_model import Post
from app.schemas.post_schema import PostCreate

class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_posts(self, user_id: int):
        return self.db.query(Post).filter(Post.user_id == user_id).all()

    def create_post(self, post: PostCreate, user_id: int):
        db_post = Post(**post.dict(), user_id=user_id)
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post

    def delete_post(self, post_id: int, user_id: int):
        post = self.db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
        if post:
            self.db.delete(post)
            self.db.commit()
            return True
        return False