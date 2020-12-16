# coding=utf8

"""
@author: zhou.xuqi
@contact: 527898116@qq.com
@time: 2018/12/22
"""
"""
对于程序log的配置
"""
import logging
from logging.config import dictConfig


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default_formatter': {
            'format': '%(asctime)s %(levelname)8s %(threadName)15s --- [%(name)s] : %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default_formatter'
        },
        'null': {
            'class': 'logging.NullHandler'
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default_formatter',
            # 'maxBytes': 50*1024*1024,
            'backupCount': 0,
            'filename': 'xxx.log',
            "when": "D",
        },
    },
    'loggers': {
        'sp': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': 0,
        },
        'sp_sender': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': 0,
        },
        '': {
            'level': 'INFO',
            'handlers': ['console'],
        }
    }
}

def configure_logging(name):
    DEFAULT_LOGGING["handlers"]["file"]["filename"] = name
    dictConfig(DEFAULT_LOGGING)
