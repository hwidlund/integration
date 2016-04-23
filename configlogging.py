#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        configlogging.py
# Purpose:     Configure logging at multiple levels.
#
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
#
# Created:     Jan 2016
#-------------------------------------------------------------------------------
# sources
# http://www.blog.pythonlibrary.org/2014/02/11/python-how-to-create-rotating-logs/
# https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook
# https://docs.python.org/2/library/logging.config.html#logging.config.dictConfig

def ConfigLogging(logFileLocation):
    import os, logging
    from logging import handlers
    from logging import config

    LOGGING = {
        'version':1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
            }
##            'simple': {
##                'format': '%(asctime)s - %(message)s'
##            },
          },
         'handlers': {
            'debuglog': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'verbose',
                'filename': os.path.join(logFileLocation, 'debuglog.log'),
                'maxBytes': 100000,
                'backupCount': 4
            },
##            'infolog': {
##                'level': 'INFO',
##                'class': 'logging.handlers.RotatingFileHandler',
##                'formatter': 'simple',
##                'filename': os.path.join(logFileLocation, 'infolog.log'),
##                'maxBytes': 1000000
##                'backupCount': 4
##             },
             'warnlog': {
                'level': 'WARNING',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'verbose',
                'filename': os.path.join(logFileLocation,'warnlog.log'),
                'maxBytes': 100000,
                'backupCount': 4
              }
         },
         'loggers': {
            'logger': {
                'level': 'DEBUG',
                'handlers': [ 'debuglog','warnlog']
            }

         }
    }

    logging.config.dictConfig(LOGGING)