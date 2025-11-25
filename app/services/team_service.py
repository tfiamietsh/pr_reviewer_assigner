from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import TeamModel
from ..orm import TeamOrm, UserOrm


class TeamService:
    @staticmethod
    async def add(
            db: AsyncSession,
            team: TeamModel
    ) -> TeamModel or None:
        team_orm = await db.execute(
            select(TeamOrm)
            .filter(TeamOrm.team_name == team.team_name)
        )

        if team_orm.scalars().first() is not None:
            return None

        members_orm = [
            UserOrm(
                user_id=member.user_id,
                username=member.username,
                is_active=member.is_active
            ) for member in team.members
        ]
        team_orm = TeamOrm(team_name=team.team_name, members=members_orm)

        db.add(team_orm)
        await db.commit()
        await db.refresh(team_orm)

        return TeamModel.from_orm(team_orm)

    @staticmethod
    async def get_by_name(
            db: AsyncSession,
            team_name: str
    ) -> TeamModel or None:
        team_orm = await db.execute(
            select(TeamOrm)
            .filter(TeamOrm.team_name == team_name)
        )
        team_orm = team_orm.scalars().first()

        if team_orm is None:
            return None

        return TeamModel.from_orm(team_orm)
