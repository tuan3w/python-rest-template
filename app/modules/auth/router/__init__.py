
from fastapi import APIRouter, status

from app.modules.auth.router.login import login
from app.modules.auth.router.me import me
from app.modules.auth.router.register import register

# router = APIRouter(prefix="/auth", tags=["auth"])
from .router import router

# router.add_api_route(
#     path="/login",
#     endpoint=login,
#     methods=["POST"],
#     status_code=status.HTTP_200_OK,
# )

# router.add_api_route(
#     path="/me",
#     endpoint=me,
#     methods=["GET"],
#     status_code=status.HTTP_200_OK,
# )

# router.add_api_route(
#     path="/register",
#     endpoint=register,
#     methods=["POST"],
#     status_code=status.HTTP_200_OK,
# )
