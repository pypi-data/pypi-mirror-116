from datetime import datetime
from json import dumps
from logging import DEBUG, INFO, Filter, Formatter
from logging.config import dictConfig
from sys import stdout


class CustomFilter(Filter):
    def filter(self, record):
        return True


class BaseFormatter(Formatter):
    def formatTime(self, record, datefmt=None):
        created = datetime.utcfromtimestamp(record.created)
        return created.isoformat()


class JsonFormatter(BaseFormatter):
    def __init__(self, _, *args, **kwargs):
        super().__init__(
            dumps(
                {
                    "time": "%(asctime)s",
                    "level": "%(levelname)s",
                    "message": "%(message)s",
                }
            ),
            *args,
            **kwargs
        )

    def format(self, record):
        return super().format(record)


class TextFormatter(BaseFormatter):
    def __init__(self, _, *args, **kwargs):
        super().__init__("%(asctime)s %(levelname)s %(message)s", *args, **kwargs)

    def format(self, record):
        return super().format(record)


def configure_loggers():
    dictConfig(
        {
            "version": 1,
            "filters": {
                "custom": {
                    "()": "air_kit.logging.CustomFilter",
                },
            },
            "formatters": {
                "json": {
                    "class": "air_kit.logging.JsonFormatter",
                },
                "text": {
                    "class": "air_kit.logging.TextFormatter",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": DEBUG,
                    "filters": ("custom",),
                    "formatter": "text",
                    "stream": stdout,
                },
            },
            "loggers": {
                "": {
                    "level": DEBUG,
                    "filters": ("custom",),
                    "handlers": ("console",),
                    "propagate": True,
                },
                "urllib3.connectionpool": {
                    "level": INFO,
                    "filters": ("custom",),
                    "handlers": ("console",),
                    "propagate": True,
                },
                "docker.utils.config": {
                    "level": INFO,
                    "filters": ("custom",),
                    "handlers": ("console",),
                    "propagate": True,
                },
                "asyncpgsa.query": {
                    "level": INFO,
                    "filters": ("custom",),
                    "handlers": ("console",),
                    "propagate": True,
                },
            },
        }
    )
