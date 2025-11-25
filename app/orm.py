from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy import DateTime, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .enums import PullRequestStatus

Base = declarative_base()


pull_request_reviewers_table = Table(
    "pull_request_reviewers",
    Base.metadata,
    Column(
        "pull_request_id",
        String,
        ForeignKey("pull_requests.pull_request_id")
    ),
    Column("user_id", String, ForeignKey("users.user_id"))
)


class UserOrm(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    team = relationship("TeamOrm", back_populates="users")
    authoring_pull_requests = relationship(
        "PullRequestOrm",
        back_populates="author"
    )
    reviewing_pull_requests = relationship(
        "PullRequestOrm",
        secondary=pull_request_reviewers_table,
        back_populates="assigned_reviewers",
        lazy="select"
    )


class TeamOrm(Base):
    __tablename__ = "teams"

    team_name = Column(String, primary_key=True)
    members = relationship(
        "UserOrm",
        back_populates="team",
        lazy="select"
    )


class PullRequestOrm(Base):
    __tablename__ = "pull_requests"

    pull_request_id = Column(String, primary_key=True)
    pull_request_name = Column(String, nullable=False)
    status = Column(Enum(PullRequestStatus), nullable=False)
    author_id = Column(String, ForeignKey("users.user_id"))
    author = relationship(
        "UserOrm",
        back_populates="authoring_pull_requests",
        lazy="select"
    )
    created_at = Column(DateTime, nullable=True)
    merged_at = Column(DateTime, nullable=True)
    assigned_reviewers = relationship(
        "UserOrm",
        secondary=pull_request_reviewers_table,
        back_populates="reviewing_pull_requests",
        lazy="select"
    )
