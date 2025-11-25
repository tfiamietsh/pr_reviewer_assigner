from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Mapped, mapped_column
from .enums import PullRequestStatus

Base = declarative_base()


class ReviewersOrm(Base):
    __tablename__ = "reviewers"

    id: Mapped[int] = mapped_column(primary_key=True)
    pull_request_id: Mapped[str] = mapped_column(
        ForeignKey("pull_requests.pull_request_id")
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.user_id")
    )


class UserOrm(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column()
    team_name: Mapped[Optional[str]] = mapped_column(
        ForeignKey("teams.team_name")
    )
    team: Mapped[Optional["TeamOrm"]] = relationship(
        "TeamOrm", back_populates="members"
    )
    authoring_pull_requests: Mapped[Optional[list["PullRequestOrm"]]] = \
        relationship(
            "PullRequestOrm",
            back_populates="author",
            lazy="select"
        )
    reviewing_pull_requests: Mapped[Optional[list["PullRequestOrm"]]] = \
        relationship(
            "ReviewersOrm",
            back_populates="user_id",
            lazy="select"
        )


class TeamOrm(Base):
    __tablename__ = "teams"

    team_name: Mapped[str] = mapped_column(primary_key=True)
    members: Mapped[list["UserOrm"]] = relationship(
        "UserOrm",
        back_populates="team",
        lazy="select"
    )


class PullRequestOrm(Base):
    __tablename__ = "pull_requests"

    pull_request_id: Mapped[str] = mapped_column(primary_key=True)
    pull_request_name: Mapped[str] = mapped_column()
    status: Mapped[PullRequestStatus] = mapped_column()
    author_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    author: Mapped["UserOrm"] = relationship(
        "UserOrm", back_populates="authoring_pull_requests"
    )
    created_at: Mapped[Optional[datetime]] = mapped_column()
    merged_at: Mapped[Optional[datetime]] = mapped_column()
    assigned_reviewers = relationship(
        "ReviewersOrm",
        back_populates="pull_request_id",
        lazy="select"
    )
