from datetime import datetime
from typing import Mapping, Optional

from pydantic import BaseModel, Field, HttpUrl


class File(BaseModel):
    filename: Optional[str]
    type: Optional[str]
    language: Optional[str]
    raw_url: Optional[HttpUrl]
    size: Optional[int]


class User(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    login: str = Field(..., examples=["octocat"])
    id: int = Field(..., examples=[1])
    node_id: str = Field(..., examples=["MDQ6VXNlcjE="])
    avatar_url: HttpUrl = Field(
        ..., examples=["https://github.com/images/error/octocat_happy.gif"]
    )
    gravatar_id: Optional[str] = Field(
        ..., examples=["41d064eb2195891e12d0413f63227ea7"]
    )
    url: HttpUrl = Field(..., examples=["https://api.github.com/users/octocat"])
    html_url: HttpUrl = Field(..., examples=["https://github.com/octocat"])
    followers_url: HttpUrl = Field(
        ..., examples=["https://api.github.com/users/octocat/followers"]
    )
    following_url: str = Field(
        ..., examples=["https://api.github.com/users/octocat/following{/other_user}"]
    )
    gists_url: str = Field(
        ..., examples=["https://api.github.com/users/octocat/gists{/gist_id}"]
    )
    starred_url: str = Field(
        ..., examples=["https://api.github.com/users/octocat/starred{/owner}{/repo}"]
    )
    subscriptions_url: HttpUrl = Field(
        ..., examples=["https://api.github.com/users/octocat/subscriptions"]
    )
    organizations_url: HttpUrl = Field(
        ..., examples=["https://api.github.com/users/octocat/orgs"]
    )
    repos_url: HttpUrl = Field(
        ..., examples=["https://api.github.com/users/octocat/repos"]
    )
    events_url: str = Field(
        ..., examples=["https://api.github.com/users/octocat/events{/privacy}"]
    )
    received_events_url: HttpUrl = Field(
        ..., examples=["https://api.github.com/users/octocat/received_events"]
    )
    type: str = Field(..., examples=["User"])
    site_admin: bool
    starred_at: Optional[datetime] = Field(None, examples=['"2020-07-09T00:17:55Z"'])


class Gist(BaseModel):
    url: HttpUrl
    forks_url: HttpUrl
    commits_url: HttpUrl
    id: str
    node_id: str
    git_pull_url: HttpUrl
    git_push_url: HttpUrl
    html_url: HttpUrl
    files: Mapping[str, File]
    public: bool
    created_at: datetime
    updated_at: datetime
    description: Optional[str]
    comments: int
    user: Optional[User]
    comments_url: HttpUrl
    owner: Optional[User] = None
    truncated: Optional[bool] = None
