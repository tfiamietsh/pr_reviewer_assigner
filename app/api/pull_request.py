from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..enums import Error
from ..services import PullRequestService
from ..models import PullRequestCreateModel

router = APIRouter()


@router.post("/create")
async def create_pr(
        pr: PullRequestCreateModel,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    pr, error = await PullRequestService.add(db, pr)

    if pr is None:
        if error == Error.PR_EXISTS:
            raise HTTPException(status_code=409, detail=error.details)
        else:
            raise HTTPException(status_code=404, detail=error.details)
    return JSONResponse(
        content=pr.model_dump(mode="json"),
        status_code=201
    )


@router.post("/merge")
async def merge_pr(
        pull_request_id: str,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    pr = await PullRequestService.merge(db, pull_request_id)

    if pr is None:
        raise HTTPException(
            status_code=404,
            detail=Error.PR_NOT_FOUND.details
        )
    return JSONResponse(content=pr.model_dump(mode="json"))


@router.post("/reassign")
async def reassign_pr(
        pull_request_id: str,
        old_user_id: str,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    pr, error = await PullRequestService.reassign(
        db, pull_request_id, old_user_id
    )

    if pr is None:
        if error == Error.PR_NOT_FOUND or error == Error.USER_NOT_FOUND:
            raise HTTPException(status_code=404, detail=error.details)
        else:
            raise HTTPException(status_code=409, detail=error.details)
    return JSONResponse(content=pr.model_dump(mode="json"))
