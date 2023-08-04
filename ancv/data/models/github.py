"""This module contains models for the relevant parts of GitHub's API."""

import typing as t
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class File(BaseModel):
    """Modelling a GitHub gist's file.

    See: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#list-gists-for-the-authenticated-user, under the "files" key.
    """

    filename: str | None = None
    type: str | None = None
    language: str | None = None
    raw_url: HttpUrl | None = None
    size: int | None = None


class GistUser(BaseModel):
    """Modelling a GitHub gist's owner/user.

    See: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#list-gists-for-the-authenticated-user
    """

    name: str | None = None
    email: str | None = None
    login: t.Annotated[str, Field(examples=["octocat"])]
    id: t.Annotated[int, Field(examples=[1])]
    node_id: t.Annotated[str, Field(examples=["MDQ6VXNlcjE="])]
    avatar_url: t.Annotated[HttpUrl, Field(examples=["https://github.com/images/error/octocat_happy.gif"])]
    gravatar_id: t.Annotated[str | None, Field(examples=["41d064eb2195891e12d0413f63227ea7"])] = None
    url: t.Annotated[HttpUrl, Field(examples=["https://api.github.com/users/octocat"])]
    html_url: t.Annotated[HttpUrl, Field(examples=["https://github.com/octocat"])]
    followers_url: t.Annotated[HttpUrl, Field(examples=["https://api.github.com/users/octocat/followers"])]
    following_url: t.Annotated[str, Field(examples=["https://api.github.com/users/octocat/following{/other_user}"])]
    gists_url: t.Annotated[str, Field(examples=["https://api.github.com/users/octocat/gists{/gist_id}"])]
    starred_url: t.Annotated[str, Field(examples=["https://api.github.com/users/octocat/starred{/owner}{/repo}"])]
    subscriptions_url: t.Annotated[HttpUrl, Field(examples=["https://api.github.com/users/octocat/subscriptions"])]
    organizations_url: t.Annotated[HttpUrl, Field(examples=["https://api.github.com/users/octocat/orgs"])]
    repos_url: t.Annotated[HttpUrl, Field(examples=["https://api.github.com/users/octocat/repos"])]
    events_url: t.Annotated[str, Field(examples=["https://api.github.com/users/octocat/events{/privacy}"])]
    received_events_url: t.Annotated[HttpUrl, Field(examples=["https://api.github.com/users/octocat/received_events"])]
    type: t.Annotated[str, Field(examples=["User"])]
    site_admin: bool
    starred_at: t.Annotated[datetime | None, Field(examples=['"2020-07-09T00:17:55Z"'])] = None


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
    files: t.Mapping[str, File]
    public: bool
    created_at: datetime
    updated_at: datetime
    description: str | None = None
    comments: int
    user: GistUser | None = None
    comments_url: HttpUrl
    owner: GistUser | None = None
    truncated: bool | None = None
