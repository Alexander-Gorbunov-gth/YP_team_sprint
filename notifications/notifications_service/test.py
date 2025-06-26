from typing import Literal
from enum import Enum


class ChannelTypes(str, Enum):
    EMAIL = "email"
    PUSH = "push"


print(list(ChannelTypes))
