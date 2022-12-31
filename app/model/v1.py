import os
from datetime import datetime
from pydantic import BaseModel, Field
import gitinfo


def get_datetime() -> str:
    return datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')


class Ping(BaseModel):
    agent: str = Field(...)
    datetime: str = Field(default_factory=get_datetime)
    message: str = "pong"


def get_gitinfo() -> str:
    return gitinfo.get_git_info()["commit"][:7]


class Project(BaseModel):
    name: str = os.getenv("NAME")
    description: str = os.getenv("DESCRIPTION")
    language: str = os.getenv("LANGUAGE")
    url: str = os.getenv("URL")
    git_hash: str = Field(default_factory=get_gitinfo)
    version: str = os.getenv("VERSION")


class Info(BaseModel):
    project: Project = Field(default_factory=Project)
