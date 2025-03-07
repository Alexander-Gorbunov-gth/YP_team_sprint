from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.services.authh.black_list import get_black_list_service, BlackList
from src.services.authh.exceptions import SessionHasExpired
from src.schemas.users import Payload
from src.services.authh.tokens import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def extract_and_validate_token(
    token: str = Depends(oauth2_scheme),
    black_list_service: BlackList = Depends(get_black_list_service),
) -> Payload:
    """
    Извлекает и валидирует JWT токен из заголовков запроса.

    :param request: HTTP запрос, содержащий токен.
    :param black_list_service: Сервис для проверки чёрного списка токенов.
    :return: Объект TokenUserData с полезной нагрузкой токена.
    """

    payload = decode_token(token)
    if await black_list_service.check_id_in_black_list(payload.jti):
        raise SessionHasExpired
    return payload
