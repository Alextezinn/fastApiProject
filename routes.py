from fastapi import APIRouter

from fastApiProject import views


routes = APIRouter()

routes.include_router(views.router, prefix="/api/v1")