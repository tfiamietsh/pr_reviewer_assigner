from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from .main import app
from .db import get_db
from .enums import Error
from .services import TeamService, UserService, PullRequestService
from .models import TeamModel, UserModel, PullRequestCreateModel


@app.post("/team/add")
async def add_team(
        team: TeamModel,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    team = await TeamService.add(db, team)

    if team is None:
        raise HTTPException(status_code=400, detail=Error.TEAM_EXISTS.value)
    return JSONResponse(content=team, status_code=201)


@app.get("/team/get")
async def get_team(
        team_name: str,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    team = await TeamService.get_by_name(db, team_name)

    if team is None:
        raise HTTPException(
            status_code=404,
            detail=Error.TEAM_NOT_FOUND.value
        )
    return JSONResponse(content=team)


@app.get("/users/add")
async def add_user(
        user: UserModel,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    user = await UserService.add(db, user)

    if user is None:
        raise HTTPException(status_code=400, detail=Error.USER_EXISTS.value)
    return JSONResponse(content=user, status_code=201)


@app.get("/users/setIsActive")
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


@app.get("/users/getReview")
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


@app.post("/pullRequest/create")
async def create_pr(
        pr: PullRequestCreateModel,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    pr, error = await PullRequestService.add(db, pr)

    if pr is None:
        if error == Error.PR_EXISTS:
            raise HTTPException(status_code=409, detail=error.value)
        else:
            raise HTTPException(status_code=404, detail=error.value)
    return JSONResponse(content=pr, status_code=201)


@app.post("/pullRequest/merge")
async def merge_pr(
        pull_request_id: str,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    pr = await PullRequestService.merge(db, pull_request_id)

    if pr is None:
        raise HTTPException(
            status_code=404,
            detail=Error.PR_NOT_FOUND.value
        )
    return JSONResponse(content=pr)


@app.post("/pullRequest/reassign")
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
            raise HTTPException(status_code=404, detail=error.value)
        else:
            raise HTTPException(status_code=409, detail=error.value)
    return JSONResponse(content=pr)
