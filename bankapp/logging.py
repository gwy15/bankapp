import logging
from logging.config import dictConfig
from pathlib import Path


LOGGING_PATH = Path('logs')
LOGGING_PATH.mkdir(exist_ok=True, parents=True)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_fmt': {
            'format': '({asctime}) - [{levelname}] {message}',
            'style': '{',
        },
        'file_fmt': {
            'format': '({asctime}) - [{levelname}] @{name}:{lineno} '
                      '[p_{process:d} t_{thread:d}] - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_fmt',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'file_fmt',
            'filename': (LOGGING_PATH / 'server.log'),
            'maxBytes': 10_000_000,
            'backupCount': 7,
            'encoding': 'utf8',
        }
    },
    'loggers': {
        'bankapp': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


def init_logging():
    dictConfig(LOGGING)
