from typing import Literal


class ChannelTypes:
    EMAIL = "email"
    PUSH = "push"
    ALL: tuple[str, ...] = (EMAIL, PUSH)
