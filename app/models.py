from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .enums import PullRequestStatus


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    username: str
    is_active: bool


class TeamModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    team_name: str
    members: list[UserModel]


class PullRequestModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pull_request_id: str
    pull_request_name: str
    author: UserModel
    status: PullRequestStatus
    created_at: datetime
    merged_at: datetime
    assigned_reviewers: list[UserModel]


class PullRequestShortModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pull_request_id: str
    pull_request_name: str
    author: UserModel
    status: PullRequestStatus
    assigned_reviewers: list[UserModel]


class PullRequestCreateModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pull_request_id: str
    pull_request_name: str
    author_id: str


class ReassignedResultModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pr: PullRequestShortModel
    replaced_by: str


class ReviewingResultModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    pull_requests: list[PullRequestShortModel]
