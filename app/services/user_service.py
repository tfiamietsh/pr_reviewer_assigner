from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import UserModel
from ..orm import UserOrm


class UserService:
    @staticmethod
    async def add(db: AsyncSession, user: UserModel) -> UserModel or None:
        user_orm = await db.execute(
            select(UserOrm)
            .filter(UserOrm.user_id == user.user_id)
        )

        if user_orm.scalars().first() is not None:
            return None

        user_orm = UserOrm(
            user_id=user.user_id,
            username=user.username,
            is_active=user.is_active
        )

        db.add(user_orm)
        await db.commit()
        await db.refresh(user_orm)

        return UserModel.from_orm(user_orm)

    @staticmethod
    async def set_is_active(
            db: AsyncSession,
            user_id: str,
            is_active: bool
    ) -> UserModel or None:
        user_orm = await db.execute(
            select(UserOrm)
            .filter(UserOrm.user_id == user_id)
        )
        user_orm = user_orm.scalars().first()

        if user_orm is None:
            return None

        user_orm.is_active = is_active
        await db.commit()
        await db.refresh(user_orm)

        return UserModel.from_orm(user_orm)

    @staticmethod
    async def get_by_id(
            db: AsyncSession,
            user_id: str
    ) -> UserModel or None:
        user_orm = await db.execute(
            select(UserOrm)
            .filter(UserOrm.user_id == user_id)
        )
        user_orm = user_orm.scalars().first()

        if user_orm is None:
            return None

        return UserModel.from_orm(user_orm)
