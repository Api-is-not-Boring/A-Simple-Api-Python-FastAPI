from os import getenv
from typing import Any
from datetime import datetime
from pydantic import BaseModel, BaseSettings, Field
from gitinfo import get_git_info


def get_datetime() -> str:
    return datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")


class Ping(BaseModel):
    agent: str = Field(...)
    datetime: str = Field(default_factory=get_datetime)
    message: str = Field("pong")


def get_git_hash() -> str:
    return get_git_info()["commit"][:7]


class Project(BaseSettings):
    name: str = Field(..., env="NAME")
    description: str = Field(..., env="DESCRIPTION")
    language: str = Field(..., env="LANGUAGE")
    url: str = Field(..., env="URL")
    git_hash: str = Field(default_factory=get_git_hash)
    version: str = Field(..., env="VERSION")

    class Config:
        env_file = ".env"


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
            remote="0.0.0.0:" + str(c.raddr[1]) if c.raddr[0] == "" else ":".join(map(str, c.raddr))
        ))
    return connections


class Connections(BaseModel):
    connections: list[Connection] = Field(default_factory=get_connections)
