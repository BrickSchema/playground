from beanie import Document
from typing import Literal

class PermissionProfile(Document):
    name: str = ""
    type: Literal["app", "user"] = "user"
    read: str
    write: str
    arguments: dict[str, str] = {}

    class Settings:
        name = "profiles"
