import logging
import pathlib

from pydantic import AnyUrl, BaseConfig, Field, computed_field
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


class DatabaseTimescaleDBSettings(BaseSettings):
    TIMESCALE_HOST: str = Field(default="localhost", description="TimescaleDB host")
    TIMESCALE_PORT: int = Field(default=5432, description="TimescaleDB port")
    TIMESCALE_USERNAME: str = Field(
        default="bricker", description="TimescaleDB username"
    )
    TIMESCALE_PASSWORD: str = Field(
        default="brick-demo", description="TimescaleDB password"
    )
    TIMESCALE_DATABASE: str = Field(default="brick", description="TimescaleDB database")


class DatabaseInfluxDBSettings(BaseSettings):
    INFLUXDB_URL: str = Field(
        default="https://us-east-1-1.aws.cloud2.influxdata.com",
        description="InfluxDB URL",
    )
    INFLUXDB_TOKEN: str = Field(
        default="", dtype="str", description="InfluxDB access token"
    )
    INFLUXDB_ORG: str = Field(
        default="9d4d3af8fd50fcbb", description="InfluxDB org name"
    )
    INFLUXDB_BUCKET: str = Field(default="CO2-Exp", description="InfluxDB bucket")


class DatabaseRedisSettings(BaseSettings):
    REDIS_HOST: str = Field(default="localhost", description="Redis host")
    REDIS_PORT: int = Field(default=6379, description="Redis port")
    REDIS_PASSWORD: str = Field(default="brick-demo", description="Redis password")
    REDIS_DATABASE: int = Field(default=0, description="Redis database index")


class DatabaseGraphDBSettings(BaseSettings):
    GRAPHDB_HOST: str = Field(default="localhost", description="GraphDB host")
    GRAPHDB_PORT: int = Field(default=7200, description="GraphDB port")
    GRAPHDB_REPOSITORY: str = Field(
        default="brickserver", description="GraphDB repository"
    )


class DatabaseSettings(
    DatabaseMongoDBSettings,
    DatabaseTimescaleDBSettings,
    DatabaseInfluxDBSettings,
    DatabaseRedisSettings,
    DatabaseGraphDBSettings,
):
    pass


class AuthGeneralSettings(BaseSettings):
    API_TOKEN: str = Field(default="YOUR-API-TOKEN", description="API token")
    AUTH_TOKEN: str = Field(
        default="YOUR-AUTHENTICATION-TOKEN", description="Authentication token"
    )
    JWT_SECRET_KEY: str = Field(
        default="YOUR-JWT-SECRET-KEY", description="JWT secret key"
    )
    JWT_SUBJECT: str = Field(default="brick", description="JWT subject")
    JWT_TOKEN_PREFIX: str = Field(default="brick", description="JWT token prefix")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_MIN: int = Field(default=0, description="JWT expiration minute")
    JWT_HOUR: int = Field(default=0, description="JWT expiration hour")
    JWT_DAY: int = Field(default=14, description="JWT expiration day")

    @computed_field
    @property
    def JWT_EXPIRE_SECONDS(self) -> int:
        return ((self.JWT_DAY * 24 + self.JWT_HOUR) * 60 + self.JWT_MIN) * 60

    # JAAS_APP_ID: str = decouple.config("JAAS_APP_ID", cast=str, default="YOUR-JAAS-APP-ID")  # type: ignore
    # JAAS_API_KEY: str = decouple.config("JAAS_API_KEY", cast=str, default="YOUR-JAAS-API-KEY")  # type: ignore
    # JAAS_PRIVATE_KEY_PATH: str = decouple.config(
    #     "JAAS_PRIVATE_KEY_PATH", cast=str, default="YOUR-JAAS-PRIVATE-KEY-PATH"
    # )  # type: ignore
    # HASHING_ALGORITHM_LAYER_1: str = decouple.config(
    #     "HASHING_ALGORITHM_LAYER_1", cast=str, default="bcrypt"
    # )  # type: ignore
    # HASHING_ALGORITHM_LAYER_2: str = decouple.config(
    #     "HASHING_ALGORITHM_LAYER_2", cast=str, default="argon2"
    # )  # type: ignore
    # HASHING_SALT: str = decouple.config("HASHING_SALT", cast=str, default="YOUR-RANDOM-SALTY-SALT")  # type: ignore


class AuthCORSSettings(BaseSettings):
    IS_ALLOWED_CREDENTIALS: bool = Field(
        default=True, description="CORS allowed credentials"
    )
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",  # React default port
        "http://0.0.0.0:3000",
        "http://127.0.0.1:3000",  # React docker port
        "http://127.0.0.1:3001",
        "http://localhost:5173",  # Qwik default port
        "http://0.0.0.0:5173",
        "http://127.0.0.1:5173",  # Qwik docker port
        "http://127.0.0.1:5174",
    ]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]


class AuthGoogleOAuthSettings(BaseSettings):
    OAUTH_GOOGLE_CLIENT_ID: str = Field(
        default="", description="Google OAuth client id"
    )
    OAUTH_GOOGLE_CLIENT_SECRET: str = Field(
        default="", description="Google OAuth client secret"
    )


class AuthSettings(AuthGeneralSettings, AuthCORSSettings, AuthGoogleOAuthSettings):
    pass


class BackendMinimalSettings(BaseSettings):
    API_PREFIX: str = "/brickapi/v1"
    DOCS_URL: str = "/brickapi/v1/docs"
    OPENAPI_URL: str = "/brickapi/v1/openapi.json"
    REDOC_URL: str = "/brickapi/v1/redoc"
    OPENAPI_PREFIX: str = ""

    SERVER_HOST: str = Field(default="0.0.0.0", description="Bind socket to this host.")
    SERVER_PORT: int = Field(
        default=9000,
        description="Bind socket to this port. "
        "If 0, an available port will be picked",
    )
    SERVER_WORKERS: int = Field(default=1, description="Number of worker processes.")
    FRONTEND_URL: str = Field(
        default=DOCS_URL,
        description="URL to frontend. Usually used for auth redirection.",
    )
    CACHE: bool = Field(default=True, description="Enable caching.")


class BackendBrickSettings(BaseSettings):
    BRICK_VERSION: str = Field(default="1.3", description="Brick version used.")
    DEFAULT_BRICK_URL: AnyUrl = Field(
        default="https://brickschema.org/schema/Brick", description="Brick schema URL."
    )
    DEFAULT_REF_SCHEMA_URL: AnyUrl = Field(
        default="https://gist.githubusercontent.com/tc-imba/714c2043e893b1538406a9113140a4fe/"
        "raw/2fa8df840f3e4f1deb647b14fe524976f004e321/ref-schema.ttl",
        description="Ref schema URL.",
    )


class BackendSettings(BackendBrickSettings, BackendMinimalSettings):
    pass


class BackendBaseSettings(DatabaseSettings, AuthSettings, BackendSettings):
    TITLE: str = "SBOS Minimal"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str = ""
    DEBUG: bool = False
    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    # # db
    # DB_MAX_POOL_CON: int = decouple.config("DB_MAX_POOL_CON", cast=int, default=5)  # type: ignore
    # DB_POOL_SIZE: int = decouple.config("DB_POOL_SIZE", cast=int, default=100)  # type: ignore
    # DB_POOL_OVERFLOW: int = decouple.config("DB_POOL_OVERFLOW", cast=int, default=80)  # type: ignore
    # DB_TIMEOUT: int = decouple.config("DB_TIMEOUT", cast=int, default=20)  # type: ignore
    # IS_DB_ECHO_LOG: bool = decouple.config("IS_DB_ECHO_LOG", cast=bool, default=False)  # type: ignore
    # IS_DB_FORCE_ROLLBACK: bool = decouple.config("IS_DB_FORCE_ROLLBACK", cast=bool, default=True)  # type: ignore
    # IS_DB_EXPIRE_ON_COMMIT: bool = decouple.config("IS_DB_EXPIRE_ON_COMMIT", cast=bool, default=True)  # type: ignore
    #
    # # s3
    # S3_HOST: str = decouple.config("S3_HOST", cast=str, default="127.0.0.1")  # type: ignore
    # S3_PORT: int = decouple.config("S3_PORT", cast=int, default=9000)  # type: ignore
    # S3_USERNAME: str = decouple.config("S3_USERNAME", cast=str, default="minioadmin")  # type: ignore
    # S3_PASSWORD: str = decouple.config("S3_PASSWORD", cast=str, default="minioadmin")  # type: ignore
    # S3_BUCKET: str = decouple.config("S3_BUCKET", cast=str, default="brick")  # type: ignore
    # S3_PUBLIC_URL: str = decouple.config("S3_PUBLIC_URL", cast=str, default="http://localhost:9000")  # type: ignore

    class Config(BaseConfig):
        case_sensitive: bool = True
        env_file: str = f"{str(ROOT_DIR)}/.env"
        validate_assignment: bool = True
        extra: str = "allow"

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | dict | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.
        """
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
            "swagger_ui_parameters": {"docExpansion": "none"},
        }
