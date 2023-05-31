from copy import deepcopy
from enum import Enum
from typing import Any, Dict, List

from pydantic import BaseModel, ConstrainedInt, Field, conlist


class PermissionProfile(BaseModel):
    class Config:
        orm_mode = True

    read: str = Field(..., description="Read template of the profile")
    write: str = Field(..., description="Write template of the profile")
