from typing import List

from fastapi import APIRouter

from fastApiProject import services
from fastApiProject.schemas import Post


router = APIRouter()


@router.get("/posts", response_model=List[Post])
async def posts(page: int=1, theme: str="", rating: str="", q: str=""):
    return await services.get_posts(page, theme, rating, q)
