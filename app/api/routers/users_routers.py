from typing import Dict
from fastapi import APIRouter, Depends
from app.api.schemas.user_schema import UserSchema

from app.api.security import get_current_active_user

from app.api.utils import ml_4xx_responses

router = APIRouter(tags=["Users"])


@router.get(
    "/me", responses=ml_4xx_responses,
)
async def get_logged_in_user_details(
    current_user: UserSchema = Depends(get_current_active_user),
):

    return current_user
