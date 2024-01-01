"""This module contains models for the relevant parts of GitHub's API."""

import typing as t
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class File(BaseModel):
    """Modelling a GitHub gist's file.

    See: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#list-gists-for-the-authenticated-user, under the "files" key.
    """

    filename: t.Optional[str] = None
    type: t.Optional[str] = None
    language: t.Optional[str] = None
    raw_url: t.Optional[HttpUrl] = None
    size: t.Optional[int] = None


class GistUser(BaseModel):
    """Modelling a GitHub gist's owner/user.

    See: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#list-gists-for-the-authenticated-user
    """

    name: t.Optional[str] = None
    email: t.Optional[str] = None
    login: t.Annotated[str, Field(examples=["octocat"])]
    id: t.Annotated[int, Field(examples=[1])]
    node_id: t.Annotated[str, Field(examples=["MDQ6VXNlcjE="])]
    avatar_url: t.Annotated[
        HttpUrl, Field(examples=["https://github.com/images/error/octocat_happy.gif"])
    ]
    gravatar_id: t.Annotated[
        t.Optional[str], Field(examples=["41d064eb2195891e12d0413f63227ea7"])
    ]
    url: t.Annotated[HttpUrl, Field(examples=["https://api.github.com/users/octocat"])]
    html_url: t.Annotated[HttpUrl, Field(examples=["https://github.com/octocat"])]
    followers_url: t.Annotated[
        HttpUrl, Field(examples=["https://api.github.com/users/octocat/followers"])
    ]
    following_url: t.Annotated[
        str,
        Field(examples=["https://api.github.com/users/octocat/following{/other_user}"]),
    ]
    gists_url: t.Annotated[
        str, Field(examples=["https://api.github.com/users/octocat/gists{/gist_id}"])
    ]
    starred_url: t.Annotated[
        str,
        Field(examples=["https://api.github.com/users/octocat/starred{/owner}{/repo}"]),
    ]
    subscriptions_url: t.Annotated[
        HttpUrl, Field(examples=["https://api.github.com/users/octocat/subscriptions"])
    ]
    organizations_url: t.Annotated[
        HttpUrl, Field(examples=["https://api.github.com/users/octocat/orgs"])
    ]
    repos_url: t.Annotated[
        HttpUrl, Field(examples=["https://api.github.com/users/octocat/repos"])
    ]
    events_url: t.Annotated[
        str, Field(examples=["https://api.github.com/users/octocat/events{/privacy}"])
    ]
    received_events_url: t.Annotated[
        HttpUrl,
        Field(examples=["https://api.github.com/users/octocat/received_events"]),
    ]
    type: t.Annotated[str, Field(examples=["User"])]
    site_admin: bool
    starred_at: t.Annotated[
        t.Optional[datetime], Field(None, examples=['"2020-07-09T00:17:55Z"'])
    ]


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
    description: t.Optional[str] = None
    comments: int
    user: t.Optional[GistUser] = None
    comments_url: HttpUrl
    owner: t.Optional[GistUser] = None
    truncated: t.Optional[bool] = None
