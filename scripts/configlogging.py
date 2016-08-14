#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        configlogging.py
# Purpose:     Configure logging at multiple levels.
#
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
#
# Created:     Jan 2016
#              Revised Aug 14, 2016 to overwrite or append to log files,
#              depending on mode passed into function. w=overwrite, a=append
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
def ConfigLogging(logFileLocation, mode):
    import os, logging
    import logging.handlers
    import logging.config

    LOGGING = {
        'version':1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
            }
          },
         'handlers': {
            'debuglog': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': os.path.join(logFileLocation, 'debuglog.log'),
                'mode': mode
            },
             'warnlog': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': os.path.join(logFileLocation,'warnlog.log'),
                'mode': mode
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