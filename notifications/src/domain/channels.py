from enum import Enum
from typing import Literal


class ChannelTypes(str, Enum):
    EMAIL = "email"
    PUSH = "push"


ChannelLiteral = Literal[ChannelTypes.EMAIL, ChannelTypes.PUSH]
