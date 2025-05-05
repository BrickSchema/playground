import pathlib

from pydantic import Field
from pydantic_settings import BaseSettings

ROOT_DIR: pathlib.Path = pathlib.Path(
    __file__
).parent.parent.parent.parent.parent.resolve()


class DatabaseMongoDBSettings(BaseSettings):
    MONGO_HOST: str = Field(default="localhost", description="MongoDB host")
    MONGO_PORT: int = Field(default=27017, description="MongoDB port")
    MONGO_USERNAME: str = Field(default="", description="MongoDB username")
    MONGO_PASSWORD: str = Field(default="", description="MongoDB password")
    MONGO_DATABASE: str = Field(default="brickserver", description="MongoDB database")
    MONGO_SCHEMA: str = Field(
        default="mongodb", description="MongoDB schema (do not modify this)"
    )


class MonitorBaseSettings(DatabaseMongoDBSettings):
    # TITLE: str = "SBOS Monitor"
    # VERSION: str = "0.1.0"
    PLAYGROUND_HOST: str = Field(default="localhost", description="The hostname of playground server.")
    PLAYGROUND_PORT: int = Field(default=9000, description="The port of playground server")
    PLAYGROUND_JWT_TOKEN: str = Field(default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsaXV5aDk3MDYxNUBnbWFpbC5jb20iLCJhdWQiOlsiYnJpY2siXSwiZXhwIjoxNzQ2ODI1MzgyfQ.f2p6KSknZ0oWWY769mpZzZWEqDb4HK3h40WhF0Tlj7Q")
    POLLING_INTERVAL: float = Field(default=60, description="The interval of polling in seconds.")

    class Config:
        env_file: str = f"{str(ROOT_DIR)}/.env"
