#!/usr/bin/python3
"""Database connection configurations."""
from pydantic import BaseSettings
from sqlmodel import SQLModel, create_engine, Session
from event_planner.schemas.events import Event
from event_planner.schemas.users import User


class Setting(BaseSettings):
    """Settings for events planning."""

    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        """environment variable configuration setting."""

        env_file: str = "./.env"


settings: Setting = Setting()

database_file: str = "test_planner.db"
database_connection_string: str = f"sqlite:///{database_file}"
connect_args: dict[str, bool] = {"check_same_thread": False}
engine_url = create_engine(
    database_connection_string, echo=True,
    connect_args=connect_args
)


def db_conn():
    """Make connection to database."""
    SQLModel.metadata.create_all(engine_url)


def get_session():
    """Get database session."""
    with Session(engine_url) as session:
        yield session
