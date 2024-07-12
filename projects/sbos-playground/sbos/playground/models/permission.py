from beanie import Document


class PermissionProfile(Document):
    name: str = ""
    read: str
    write: str
    arguments: dict[str, str] = {}

    class Settings:
        name = "profiles"
