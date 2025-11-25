from datetime import datetime
from random import randint, sample, choice
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import PullRequestCreateModel, PullRequestShortModel
from ..models import PullRequestModel
from ..models import ReassignedResultModel, ReviewingResultModel
from ..orm import PullRequestOrm, UserOrm
from ..enums import Error, PullRequestStatus
from .user_service import UserService


class PullRequestService:
    @staticmethod
    async def add(
            db: AsyncSession,
            pr: PullRequestCreateModel
    ) -> tuple[PullRequestShortModel or None, Error or None]:
        pr_orm = await db.execute(
            select(PullRequestOrm)
            .filter(PullRequestOrm.pull_request_id == pr.pull_request_id)
        )

        if pr_orm.scalars().first() is not None:
            return None, Error.PR_EXISTS

        author_orm = await db.execute(
            select(UserOrm)
            .filter(UserOrm.user_id == pr.author_id)
        )
        author_orm = author_orm.scalars().first()

        if author_orm.scalars().first() is None:
            return None, Error.AUTHOR_NOT_FOUND

        team_orm = author_orm.team
        if team_orm is None:
            return None, Error.TEAM_NOT_FOUND

        candidates = [
            member for member in team_orm.members
            if member.user_id != author_orm.user_id and member.is_active
        ]
        k = randint(0, min(len(candidates), 2))
        reviewers = sample(candidates, k=k)

        pr_orm = PullRequestOrm(
            pull_request_id=pr.pull_request_id,
            pull_request_name=pr.pull_request_name,
            status=PullRequestStatus.OPEN,
            author=author_orm,
            created_at=datetime.now(),
            merged_at=None,
            assigned_reviewers=reviewers
        )

        db.add(pr_orm)
        await db.commit()
        await db.refresh(pr_orm)

        return PullRequestShortModel.from_orm(pr_orm), None

    @staticmethod
    async def merge(
            db: AsyncSession,
            pull_request_id: str
    ) -> PullRequestModel or None:
        pr_orm = await db.execute(
            select(PullRequestOrm)
            .filter(PullRequestOrm.pull_request_id == pull_request_id)
        )
        pr_orm = pr_orm.scalars().first()

        if pr_orm is None:
            return None

        if pr_orm.status == PullRequestStatus.OPEN:
            pr_orm.status = PullRequestStatus.MERGED
            await db.commit()
            await db.refresh(pr_orm)

        return PullRequestModel.from_orm(pr_orm)

    @staticmethod
    async def reassign(
            db: AsyncSession,
            pull_request_id: str,
            old_user_id: str
    ) -> tuple[ReassignedResultModel or None, Error or None]:
        pr_orm = await db.execute(
            select(PullRequestOrm)
            .filter(PullRequestOrm.pull_request_id == pull_request_id)
        )
        pr_orm = pr_orm.scalars().first()

        if pr_orm is None:
            return None, Error.PR_NOT_FOUND

        user_orm = await UserService.get_by_id(db, old_user_id)

        if user_orm is None:
            return None, Error.USER_NOT_FOUND

        if not user_orm.is_active:
            return None, Error.NOT_ASSIGNED

        if pr_orm.status == PullRequestStatus.MERGED:
            return None, Error.PR_MERGED

        if user_orm not in pr_orm.assigned_reviewers:
            return None, Error.REVIEWER_NOT_FOUND

        team_orm = user_orm.team
        candidates = [
            member for member in team_orm.members
            if member.user_id != pr_orm.author_id and member.is_active
        ]

        if len(candidates) == 0:
            return None, Error.NO_CANDIDATE

        reviewer_orm = choice(candidates)

        idx = 0
        for i in range(len(pr_orm.assigned_reviewers)):
            if pr_orm.assigned_reviewers[i] == user_orm:
                idx = i
                break
        pr_orm.assigned_reviewers[idx] = reviewer_orm

        await db.commit()
        await db.refresh(pr_orm)

        return ReassignedResultModel(
            pr=PullRequestShortModel.from_orm(pr_orm),
            replaced_by=old_user_id
        ), None

    @staticmethod
    async def get_by_user_id(
            db: AsyncSession,
            user_id: str
    ) -> ReviewingResultModel or None:
        user_orm = await db.execute(
            select(UserOrm)
            .filter(UserOrm.user_id == user_id)
        )
        user_orm = user_orm.scalars().first()

        if user_orm is None:
            return None

        pull_requests = [
            PullRequestShortModel.from_orm(pr_orm)
            for pr_orm in user_orm.reviewing_pull_requests
        ]

        return ReviewingResultModel(
            user_id=user_id,
            pull_requests=pull_requests
        )
