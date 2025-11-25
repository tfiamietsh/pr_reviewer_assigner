from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..enums import Error
from ..services import TeamService
from ..models import TeamModel

router = APIRouter()


@router.post("/add")
async def add_team(
        team: TeamModel,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    team = await TeamService.add(db, team)

    if team is None:
        raise HTTPException(
            status_code=400,
            detail=Error.TEAM_EXISTS.details
        )
    return JSONResponse(
        content=team.model_dump(mode="json"),
        status_code=201
    )


@router.get("/get")
async def get_team(
        team_name: str,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    team = await TeamService.get_by_name(db, team_name)

    if team is None:
        raise HTTPException(
            status_code=404,
            detail=Error.TEAM_NOT_FOUND.details
        )
    return JSONResponse(content=team.model_dump(mode="json"))
