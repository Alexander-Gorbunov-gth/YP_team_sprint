from pathlib import Path

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DEFAULT_HANDLERS = [
    "console",
    "file_warning",
]

# В логгере настраивается логгирование uvicorn-сервера.
# Про логирование в Python можно прочитать в документации
# https://docs.python.org/3/howto/logging.html
# https://docs.python.org/3/howto/logging-cookbook.html


def get_logger_settings(log_path: str | Path):
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": LOG_FORMAT,
            },
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",  # Показываем всё
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "file_warning": {
                "level": "WARNING",  # Только WARNING и выше
                "class": "logging.FileHandler",
                "formatter": "verbose",
                "filename": f"{log_path}/warnings.log",
                "encoding": "utf-8",
            },
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "handlers": LOG_DEFAULT_HANDLERS,
                "level": "DEBUG",
            },
            "uvicorn.error": {
                "level": "INFO",
            },
            "uvicorn.access": {
                "handlers": ["access"],
                "level": "INFO",
                "propagate": False,
            },
            "aio_pika": {
                "level": "INFO",
            },
            "aiormq": {
                "level": "INFO",
            },
            "elastic_transport.transport": {
                "level": "INFO",
            },
        },
        "root": {
            "level": "DEBUG",
            "formatter": "verbose",
            "handlers": LOG_DEFAULT_HANDLERS,
        },
    }
    return LOGGING
