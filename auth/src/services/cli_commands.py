import typer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.users import User
from src.core.config import settings


engine = create_engine(settings.postgres.db_sync_url)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

typer_app = typer.Typer()


@typer_app.command(name="createsuperuser")
def createsuperuser(login: str, password: str):
    """Создает нового администратора в базе данных."""
    db = session()
    try:
        existing_user = db.query(User).filter(User.login == login).first()
        if existing_user:
            typer.echo("Пользователь с таким именем уже существует.")
            return
        new_admin = User(
            login=login,
            password=password,
            is_superuser=True
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        typer.echo(f"Администратор {new_admin.login} успешно создан.")
    except Exception as e:
        db.rollback()
        typer.echo(f"Произошла ошибка: {e}")
    finally:
        db.close()


@typer_app.command(name="check")
def check(arg: str):
    typer.echo(arg)
    return
# python src/main.py createsuperuser admin admin