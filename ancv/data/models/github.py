"""This module contains models for the relevant parts of GitHub's API."""

from datetime import datetime
from typing import Mapping, Optional

from pydantic import BaseModel, Field, HttpUrl


class File(BaseModel):
    """Modelling a GitHub gist's file.

    See: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#list-gists-for-the-authenticated-user, under the "files" key.
    """

    filename: Optional[str] = None
    type: Optional[str] = None
    language: Optional[str] = None
    raw_url: Optional[HttpUrl] = None
    size: Optional[int] = None


class GistUser(BaseModel):
    """Modelling a GitHub gist's owner/user.

    See: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#list-gists-for-the-authenticated-user
    """

    name: Optional[str] = None
    email: Optional[str] = None
    login: str = Field(..., examples=["octocat"])
    id: int = Field(..., examples=[1])
    node_id: str = Field(..., examples=["MDQ6VXNlcjE="])
    avatar_url: HttpUrl = Field(
        ..., examples=["https://github.com/images/error/octocat_happy.gif"]
    )
    gravatar_id: Optional[str] = Field(
        None, examples=["41d064eb2195891e12d0413f63227ea7"]
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
    """Modelling a GitHub gist.

    See: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28"""

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
    description: Optional[str] = None
    comments: int
    user: Optional[GistUser] = None
    comments_url: HttpUrl
    owner: Optional[GistUser] = None
    truncated: Optional[bool] = None
