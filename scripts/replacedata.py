#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        replacedata.py
# Purpose:     Replace data in output file geodatabase with updated data,
#              configurations read from config file, (data sources, field names, etc.)
#              fields mapped according to field mapper
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Credits:     Portions adapted from Esri Community Addresses local Government Solution scripts
#              (http://solutions.arcgis.com/local-government/help/community-addresses/get-started/)
# Date:        Jan 2016; revised Apr 24, 2016;
# Versions:    Python 2.7.5 & ArcGIS 10.2+
#-------------------------------------------------------------------------------
# Requirements
# 0. Full path/name of *.ini file which holds the configurations.
#    See config scripts for details. i.e. configaddresspts.py
# 1. Folder location for log files (warnlog.log, debuglog.log)
# (2.) Source of data field name is coded below in buildsql function as 'SOD'
# (3.) Unique ID field name is coded as idFieldName = 'SID' below
# Helper scripts must be in same folder as this script
# Helper scripts: fieldmappings.py, appenddata.py, truncatetable.py,
#   buildsql.py, configlogging.py, validatefields.py, uniqueid.py,
#   calclatlong.py, removemetadata.py
#-------------------------------------------------------------------------------
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
import sys, os
import logging
import configlogging    ## custom function to create & configure logger object
import ConfigParser
import arcpy
from arcpy import env
import fieldmappings as createfm  ## custom function to create field mappings
import validatefields   ## custom function to validate field types & lengths
import truncatetable    ## custom function to delete all existing data records
import buildsql         ## custom function to build SQL definition query with delimiters
import appenddata       ## custom function to append data using selection set and field mappings
import uniqueid         ## custom function to check for valid and unique id values
import calclatlong      ## custom function to calculate lat and long fields
import removemetadata   ## custom function for deleting gp history & local machine name from metadata

def ReplaceIntData(config_file, log_file_location):
    # --------------------------------
    # Setup
    # check for log file location & set up logging
    if not os.path.isdir(log_file_location):
        os.mkdir(log_file_location)
    try:
        configlogging.ConfigLogging(log_file_location)
    except:
        print('log file error')
        sys.exit(1)
    logger = logging.getLogger('logger')

    # set to overwrite
    arcpy.env.overwriteOutput = True

    # check for config file
    if os.path.isfile(config_file):
        if not os.path.splitext(config_file)[1] == ".ini":
            error = "Configuration file is not a *.ini file " + str(config_file)
            logger.error(error)
            return (False,error)

        # initialize config parser object
        config = ConfigParser.ConfigParser()

        # read config file
        config.read(config_file)
    else:
        error = "Configuration file " + str(config_file) + " not found or is not a *.ini file. Exiting."
        logger.error(error)
        return (False,error)

    # --------------------------------
    # Get configurations from file for data sources, SQL & datum transformation
    logger.debug("Reading configuration file for... " + str(config_file))
    # p_val = config.get('SECTION','p_name') from config script
    try:
        inputFeatureClass = config.get('LOCAL_DATA','INPUTFC')          ## required
        outputFileGdb = config.get('LOCAL_DATA','OUTPUTFGDB')           ## required
        outputFeatureClass = config.get('LOCAL_DATA', 'OUTPUTFC')       ## required

        srcOfData = config.get('SQL_PARAMETERS','SOURCE')               ## required
        addlSql = config.get('SQL_PARAMETERS','ADDLSQL')                ## not required

        datumTransformation = config.get('SPATIAL_REF', 'DATUMTRANS')   ## required
    except ConfigParser.Error as cperror:
        error = "Config parser error " + str(cperror)
        logger.error(error)
        return (False, error)

    # check for required inputs
    if not arcpy.Exists(inputFeatureClass):
        error = str(inputFeatureClass) + " does not exist. Run the config tool. Exiting."
        logger.error(error)
        return (False,error)

    if not arcpy.Exists(outputFileGdb):
        error = str(outputFileGdb) + " does not exist. Run the config tool. Exiting."
        logger.error(error)
        return (False,error)

    if not arcpy.Exists(outputFeatureClass):
        error = str(outputFeatureClass) + " does not exist. Run the config tool. Exiting."
        logger.error(error)
        return (False,error)

    if srcOfData == '':
        error = "Please specify an SOD/source of data by running the config tool. Exiting."
        logger.error(error)
        return (False,error)

    if datumTransformation == '':
        error = "Please specify a datum transformation by running the config tool. Exiting."
        logger.error(error)
        return (False,error)

    # get feature class base names for use in logging
    descInput = arcpy.Describe(inputFeatureClass)
    inputName = descInput.baseName
    descOutput = arcpy.Describe(outputFeatureClass)
    outputName = descOutput.baseName

    # build list of fields to check input data for SOD field
    sod = "SOD"
    fieldNamesInput = [f.name for f in arcpy.ListFields(inputFeatureClass, sod)]

    # fail if SOD field does not exist in source
    if not sod in fieldNamesInput:
        error = inputName + "| Failed: check for existence of SOD field"
        logger.error(error)
        return (False,error)

    #---------------------------------
    # Field mapping: create dictionary from all field name pairs ("options" & "values")
    #   in field mapper "section" of config file
    #
    # http://stackoverflow.com/questions/8578430/python-config-parser-to-get-all-the-values-from-a-section
    # http://resources.arcgis.com/en/help/main/10.2/index.html#//002z00000014000000

    fldMapDict = dict(config.items('FIELD_MAPPER'))

    # Check for fields that are too long
    logger.debug("Checking field lengths")
    outcome = validatefields.ValidateFields(inputFeatureClass,outputFeatureClass,fldMapDict)
    if not outcome[0]:
        error = inputName + " | Failed: validate fields | " + outcome[1]
        logger.error(error)
        return (False, error)
    else:
        if not outcome[1] == "":
            logger.warning(inputName + " | " + outcome[1])
        logger.debug("Succeeded: validate fields")

    #--------------------------
    # Pass dictionary of field maps to field mapper function, return fieldMappings object
    logger.debug("Field mapping")
    outcome = createfm.CreateFieldMapping(inputFeatureClass, outputFeatureClass, fldMapDict)
    if not outcome[0]:
        error = inputName + " | Failed: field mapping | " + outcome[1]
        logger.error(error)
        return (False, error)
    else:
        logger.debug("Succeeded: field mapping  " + outcome[1])
        fieldMappings = outcome[2]

    #--------------------------
    # Delete all records in output feature class using truncate function
    logger.debug("Truncating table")
    outcome = truncatetable.Truncate(outputFeatureClass)
    if not outcome[0]:
        error = outputName + " | Failed: truncate table | " + outcome[1]
        logger.error(error)
        return (False,error)
    else:
        logger.debug("Succeeded: truncate table")

    #--------------------------
    # Set environments for append so it will project using datum transformation
    #   append respects the output coordinate system, so does the projection for us
    arcpy.env.workspace = outputFileGdb
    arcpy.env.geographicTransformations = datumTransformation

    #--------------------------
    # Build SQL query with correct delimiters; "SOD" is "source of data" field name
    logger.debug("Building SQL expression")
    outcome = buildsql.BuildSQL(inputFeatureClass, sod, srcOfData)
    whereClause = outcome[1]
    if not addlSql == '':
        whereClause = whereClause + ' ' + addlSql
    logger.debug(inputName + " | Final SQL expression: " + whereClause)

    #--------------------------
    # Append new records to output feature class using append function
    #   Fields which don't match the output schema will be mapped from above function
    #   Fields which exist in the input but not output schema will be dropped
    #   Fields that match will be automatically mapped
    logger.debug("Appending data")
    outcome = appenddata.AppendData(inputFeatureClass, outputFeatureClass, whereClause, fieldMappings)
    if not outcome[0]:
        error = inputName + " | Failed: append data | " + outcome[1]
        logger.error(error)
        return (False,error)
    logger.debug("Succeeded: append data")

    #--------------------------
    # Check output feature class for unique ids, create message if there are issues
    logger.debug("Checking for unique IDs")
    idFieldName = 'SID'

    # Build field names list to check for SID field in output data
    fieldNamesOutput = [f.name for f in arcpy.ListFields(outputFeatureClass, idFieldName)]

    if idFieldName in fieldNamesOutput:
        outcome = uniqueid.UniqueId(outputFeatureClass, idFieldName)
        if not outcome[0]:
            error = outputName + " | Failed: validate ids | " + outcome[1]
            logger.error(error)
            return (False, error)
        if not outcome[1] == "":
            logger.warning(outputName + " | " + outcome[1])
    else:
        logger.debug(outputName + " | No SID field; skipped.")
    logger.debug("Checked for unique IDs")

    #--------------------------
    # Repair output feature class geometry
    logger.debug("Repairing geometry")
    try:
        arcpy.RepairGeometry_management(outputFeatureClass)
    except Exception as e:
        logger.warning(outputName + " | Failed: repair geometry")
        logger.warning(str(e))
    logger.debug("Repaired geometry")

    #--------------------------
    # Calculate Lat Long fields
    if arcpy.Describe(outputFeatureClass).shapeType == "Point":
        logger.debug("Calculating lat and long fields")
        outcome = calclatlong.CalcLatLong(outputFeatureClass)
        if not outcome[0]:
            error = outputName + " | Failed: calculate lat and long | " + outcome[1]
            logger.error(error)
            return (False,error)
        logger.debug("Succeeded: calculate lat and long fields")

    #--------------------------
    # Strip unwanted metadata and geoprocessing history
    logger.debug("Removing unwanted metadata and gp history")
    outcome = removemetadata.RemoveUnwantedMetadata(outputFileGdb, outputFeatureClass)
    if not outcome[0]:
        error = outputName + " | Failed: remove metadata. | " + outcome[1]
        logger.error(error)
        return (False, error)
    logger.debug("Succeeded: removed unwanted metadata and gp history")

    return (True,"Succeeded")

if __name__ == '__main__':
    ReplaceIntData(sys.argv[1], sys.argv[2])
