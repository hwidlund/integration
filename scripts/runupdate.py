#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        runupdate.py
# Purpose:     Run update script "replacedata.py" for all data in a geodatabase
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Date:        Feb 2016, updated Mar 26, 2016;
# Versions:    Python 2.7.5 & ArcGIS 10.2+
#-------------------------------------------------------------------------------
# Requirements
# 0. Path to configuration files (*.ini) directory
# 1. log file location directory
# 2. Path to output data directory
#
# ------------------------------------------------------------------------------
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
import os, sys
import logging
import configlogging        ## custom function for configuring logging
import replacedata          ## custom function for replacing data
import sendmessage          ## custom function for sending notifications
import zipfgdb              ## custom function for zipping up fgdb

def Updater(configPath, logFilePath, dataPath):
    # set up logging
    if not os.path.isdir(logFilePath):
        os.mkdir(logFilePath)
    try:
        configlogging.ConfigLogging(logFilePath)
    except:
        print('log file error')
        sys.exit(1)         ## log file error
    logger = logging.getLogger('logger')

    logger.info("*-----------------------------------------------------------*")
    logger.info("Beginning updater script to update all data...")

    # T/F send error message
    sendError = False       ## this will be tripped to true if an error is encountered
    sendType = ""           ## change to "email" if using notifications, need to configure sendmessage.py

    # iterate through all ini files in configuration directory
    # call data replacement script on each one
    for root,dirs,files in os.walk(configPath):
        for f in files:
            if os.path.splitext(f)[1] == ".ini":
                logger.debug("*-----------------------------------------------------------*")
                outcome = replacedata.ReplaceIntData(os.path.join(configPath,f), logFilePath)
                if not outcome[0]:
                    error = 'Failed: replace data for ' + f + '\n' + outcome[1]
                    logger.error(error)
                    sendError = True
                else:
                    logger.debug('Succeeded: replace data for ' + f)
    logger.info('Finished updater script for all data.')
    logger.info("*-----------------------------------------------------------*")

    # zip up file geodatabase(s) if no error has been raised
    if not sendError:
        logger.debug("Zipping geodatabase")
        outcome = zipfgdb.ZipFgdb(dataPath)
        if not outcome[0]:
            logger.error(outcome[1])
            sendError = True
        else:
            logger.debug('Succeeded: zip geodatabases ' + dataPath)
    logger.info('Script complete')
    logger.info('*------------------------------------------------------------*')

    # send an email notification of success/failure
    if sendType == "email":
        if not sendError:
            outcome = sendmessage.SendEmail("Data integration scripts ran successfully.")
        else:
            outcome = sendmessage.SendEmail("Check data integration scripts warnlog.log for errors.")
        if not outcome[0]:
            logger.error(outcome[1])

    # generate exit code > batch script
    if not sendError:       ## success
        sys.exit(0)
    else:                   ## failure
        sys.exit(2)

if __name__ == '__main__':
    Updater(sys.argv[1], sys.argv[2], sys.argv[3])