#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        build_sql_exp.py
# Purpose:     Build where clause with appropriate delimiters
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Credits:     http://gis.stackexchange.com/questions/27457/including-variable-in-where-clause-of-arcpy-select-analysis
# Date:        Jan 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
#-------------------------------------------------------------------------------
import arcpy
def BuildSQL(inputFC, field, value):

    # Add appropriate delimiters
    fieldDelim = arcpy.AddFieldDelimiters(inputFC,field)

    # determine field type
    fieldType = arcpy.ListFields(inputFC, field)[0].type

    # Add single quotes for string types
    if str(fieldType) == 'String':
        value = "'{0}'".format(value)
    whereClause = "{0} = {1}".format(fieldDelim,value)

    return (True,whereClause)