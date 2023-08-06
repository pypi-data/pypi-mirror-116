from logging import config
from typing import Any, Dict

DEFAULT_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


def setup_logging(configuration: Dict[str, Any] = None):
    config.dictConfig(configuration or DEFAULT_CONFIG)
