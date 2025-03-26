from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.post_schema import PostCreate, Post
from app.services.post_service import PostService
from app.services.cache_service import cache_service
from typing import List

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=Post)
def create_post(post: PostCreate, post_service: PostService = Depends()):
    return post_service.create_post(post)


@router.get("/", response_model=List[Post])
def get_posts(request: Request, post_service: PostService = Depends()):
    user_id = str(post_service.current_user.id)
    cached_data = cache_service.get_cached_response(user_id, "get_posts")
    if cached_data:
        return cached_data

    posts = post_service.get_user_posts()
    cache_service.set_cached_response(user_id, "get_posts", posts)
    return posts


@router.delete("/{post_id}")
def delete_post(post_id: int, post_service: PostService = Depends()):
    return post_service.delete_post(post_id)