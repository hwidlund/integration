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
'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

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