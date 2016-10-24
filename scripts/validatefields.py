#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        validatefields.py
# Purpose:     Validate field lengths/types
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Date:        Jan 2016, revised Apr 20, 2016, revised Sept 5, 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
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
def ValidateFields(srcFC, destFC, fldMapDict):
    import arcpy

    # Get field lists from each feature class
    srcFields = arcpy.ListFields(srcFC)     #inputFc - agency source
    destFields = arcpy.ListFields(destFC)   #outputFc - integrated destination
    srcDict = {}
    destDict = {}
    message = ""
    error = ""

    # Build dictionaries from the field lists of each feature class
    # so they can be accessed by name as well as hold the field
    # characteristics of type and length. (Field names are in the config file &
    # the fldMapDict dictionary is built from that.)
    # For example: srcDict["SOD"] = ["String", 6]
    for srcField in srcFields:
        if not srcField.required:
            srcDict[srcField.name] = [srcField.type, srcField.length]

    for destField in destFields:
        if not destField.required:
            destDict[destField.name] = [destField.type, destField.length]

    # iterate through the field mapping dictionary
    # check for type and length mismatches
    for dfld, sfld in fldMapDict.items():
       if not sfld == '':                      ## if the destination field is *not unmatched* in source
            dfldUpper = dfld.upper()           ## uppercase the destination field name
            if dfldUpper in destDict:          ## if the destination field (from the config file) is in the
                                               ##   dictionary of destination fields (in the output feature class)
                dfldType = destDict[dfldUpper][0]  ## get the field type
                dfldLen = destDict[dfldUpper][1]   ## get the field length
            if sfld in srcDict:                ## if the source field (from the config file) is in the dictionary
                                               ## of source fields in the input feature class
                sfldType = srcDict[sfld][0]    ## get the field type
                sfldLen = srcDict[sfld][1]     ## get the field length
            if dfldType == 'String' and sfldType == 'String' and dfldLen < sfldLen: ## a fatal error: field won't append
                error += "Field length mismatch (too long): {0} < {1}\n".format(dfldUpper, sfld)
            if not dfldType == sfldType:           ## not a fatal error
                message += "Field type mismatch: {0} ({1}) & {2} ({3})\n".format(dfldUpper, dfldType, sfld, sfldType)
    if error == "":
        return (True, message)
    else:
        return (False, error)
