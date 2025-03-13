from uuid import UUID

from .session import Session


class SessionFactory:
    @staticmethod
    def create(
        user_id: UUID,
        jti: UUID,
        user_agent: str,
        refresh_token: str,
        user_ip: str | None = None,
    ) -> Session:
        return Session(
            id=None,
            user_id=user_id,
            jti=jti,
            user_agent=user_agent,
            user_ip=user_ip,
            refresh_token=refresh_token,
            created_at=None,
            updated_at=None,
        )
