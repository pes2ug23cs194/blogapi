from fastapi import APIRouter, Depends
from app.oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/")
def get_posts(current_user: int = Depends(get_current_user)):
    return {"message": f"Here are the posts for user {current_user}"}