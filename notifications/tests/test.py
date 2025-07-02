from enum import Enum
from typing import Literal


class ChannelTypes(str, Enum):
    EMAIL = "email"
    PUSH = "push"


print(ChannelTypes)

for channel in ChannelTypes:
    print(channel.value)
