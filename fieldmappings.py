#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        create_field_mappings.py
# Purpose:     Create field mappings for input -> output datasets
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Date:        Jan 2016, revised Mar 26, 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
#-------------------------------------------------------------------------------
# Requirements
# 0. Input feature class with local schema
# 1. Output feature class with target schema
# 2. Dictionary of field mapping pairs
#-------------------------------------------------------------------------------
import arcpy

def CreateFieldMapping(inputFC, outputFC, fmDict):

    fieldMappings = arcpy.FieldMappings()
    fieldMappings.addTable(inputFC)
    fieldMappings.addTable(outputFC)
    inputFields = [f.name for f in arcpy.ListFields(inputFC)]
    message = ""

    # Iterate through field mapping dictionary key/value pairs
    # Skip keys for which the value is '' (unmatched in input feature class)
    # If the key is not equal to the value, send the pair to the field mapper
    # Keys in dictionaries are always lowercase, but our fields are uppercase,
    #   so use string function .upper() to account for this
    try:
        for targetField, inputField in fmDict.items():
            if not inputField == '':
                if inputField in inputFields:
                    tField = str(targetField).upper()
                    iField = str(inputField).upper()
                    if not tField == iField:
                        message += tField + ' | ' + iField + '\n'
                        fmIndex = fieldMappings.findFieldMapIndex(tField)
                        fieldMap = fieldMappings.getFieldMap(fmIndex)
                        fieldMap.addInputField(inputFC, iField)
                        fieldMappings.replaceFieldMap(fieldMappings.findFieldMapIndex(tField), fieldMap)
                        fieldMappings.removeFieldMap(fieldMappings.findFieldMapIndex(iField))
        return (True,message,fieldMappings)
    except Exception as e:
        error = 'Failed: field mapping. ' + str(e)
        return (False,error)