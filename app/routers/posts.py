from logging import raiseExceptions

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user
from typing import List

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str = ""
):
    posts = db.query(models.Post)\
        .filter(models.Post.title.contains(search))\
        .limit(limit)\
        .offset(skip)\
        .all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_post = models.Post(owner_id=current_user, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.PostResponse)
def get_posts_by_id(id:int,db:Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="post not found "
        )
    return post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id:int,db:Session = Depends(get_db),current_user:int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="post not found "
        )
    if post.owner_id != current_user:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Can not delete this post "
        )
    db.delete(post)
    db.commit()
    return

@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.PostResponse)
def update_post_by_id(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if existing_post.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.published = post.published
    db.commit()
    db.refresh(existing_post)
    return existing_post