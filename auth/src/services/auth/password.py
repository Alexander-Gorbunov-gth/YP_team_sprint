from passlib.context import CryptContext

context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    """Хеширует пароль с использованием алгоритма."""

    return context.hash(password)


def verify_password(password: str, hashed_password) -> bool:
    """Проверяет подлинность пароля"""
    
    return context.verify(password, hashed_password)
