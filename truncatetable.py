#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        truncate_table.py
# Purpose:     Delete all old records in output feature class to prepare
#              for appending of updated records
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Date:        Jan 2016, updated Mar 25, 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
#-------------------------------------------------------------------------------
import arcpy
def Truncate(outputFC):

    # Delete all data in output feature class
    try:
        arcpy.TruncateTable_management(outputFC)
        return (True, 'Succeeded')
    except Exception as e:
        error = "Failed: truncate output feature class table. " + str(e)
        return (False, error)