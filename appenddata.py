#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        appenddata.py
# Purpose:     Append updated data to output feature class using
#              field mappings
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Date:        Jan 2016, updated Mar 25, 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
#-------------------------------------------------------------------------------
# Requirements
# 0. Input feature class with updated data
# 1. Output feature class, now empty from truncate function
# 2. Where clause to limit what gets appended
# 3. Field mappings created by field mappings function
#-------------------------------------------------------------------------------
import arcpy

def AppendData(inputFC, outputFC, whereClause, fieldMappings):

    # set to overwrite output for feature layers
    arcpy.env.overwriteOutput = True

    # Make feature layer & create selection
    flInput = 'flInput'
    try:
        arcpy.MakeFeatureLayer_management(inputFC, flInput, whereClause)
        arcpy.SelectLayerByAttribute_management(flInput, 'NEW_SELECTION', whereClause)
    except Exception as e:
        error = "Failed: make feature layer and selection with SQL where clause. " + str(e)
        del flInput
        return (False,error)

    # Append new data to old feature class with field mappings
    # Append_management   http://resources.arcgis.com/en/help/main/10.2/index.html#//001700000050000000
    try:
        arcpy.Append_management(flInput, outputFC, 'NO_TEST', fieldMappings)
        return (True, "Succeeded")
    except Exception as e:
        error = "Failed: append records to empty feature class. " + str(e)
        return (False,error)
    finally:
        del flInput