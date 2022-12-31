from os import getenv
from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field
from gitinfo import get_git_info


def get_datetime() -> str:
    return datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')


class Ping(BaseModel):
    agent: str = Field(...)
    datetime: str = Field(default_factory=get_datetime)
    message: str = Field("pong")


def get_gitinfo() -> str:
    return get_git_info()["commit"][:7]


class Project(BaseModel):
    name: str = Field(getenv("NAME"))
    description: str = Field(getenv("DESCRIPTION"))
    language: str = Field(getenv("LANGUAGE"))
    url: str = Field(getenv("URL"))
    git_hash: str = Field(default_factory=get_gitinfo)
    version: str = Field(getenv("VERSION"))


class Info(BaseModel):
    project: Project = Field(default_factory=Project)


class Connection(BaseModel):
    id: int
    protocol: str = Field("TCP")
    type: str | Any
    local: str
    remote: str


def get_connections() -> list[Connection]:
    from pypsutil import Process
    connections: list[Connection] = []
    p = Process()
    for c in p.connections():
        connections.append(Connection(
            id=c.fd,
            type=c.status.value,
            local=":".join(map(str, c.laddr)),
            remote="0.0.0.0:" + str(c.raddr[1]) if c.raddr[0].isprintable() else ":".join(map(str, c.raddr))
        ))
    return connections


class Connections(BaseModel):
    connections: list[Connection] = Field(default_factory=get_connections)
