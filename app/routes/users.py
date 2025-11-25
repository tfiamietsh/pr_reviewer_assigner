from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..enums import Error
from ..services import UserService, PullRequestService
from ..models import UserModel

router = APIRouter()


@router.post("/add")
async def add_user(
        user: UserModel,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    user = await UserService.add(db, user)

    if user is None:
        raise HTTPException(status_code=400, detail=Error.USER_EXISTS.value)
    return JSONResponse(content=user, status_code=201)


@router.post("/setIsActive")
async def set_user_is_active(
        user_id: str,
        is_active: bool,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    user = await UserService.set_is_active(db, user_id, is_active)

    if user is None:
        raise HTTPException(
            status_code=400,
            detail=Error.USER_NOT_FOUND.value
        )
    return JSONResponse(content=user, status_code=201)


@router.get("/getReview")
async def get_reviewing_prs(
        user_id: str,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    result = await PullRequestService.get_by_user_id(db, user_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=Error.USER_NOT_FOUND.value
        )
    return JSONResponse(content=result)
