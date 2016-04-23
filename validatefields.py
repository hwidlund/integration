#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        validatefields.py
# Purpose:     Validate field lengths/types
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Date:        Jan 2016, revised Apr 20, 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
#-------------------------------------------------------------------------------
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
    # For example: srcDict["SOD"] = ["String", 20]
    for srcField in srcFields:
        srcDict[srcField.name] = [srcField.type, srcField.length]

    for destField in destFields:
        destDict[destField.name] = [destField.type, destField.length]

    # iterate through the field mapping dictionary
    # check for type and length mismatches
    for dfld, sfld in fldMapDict.items():
       if not sfld == '':                          ## if the destination field is *not unmatched* in source
            dfldUpper = dfld.upper()               ## uppercase the destination field name (is all lowercase in key/value pair in config file)
            if dfldUpper in destDict and sfld in srcDict:  ## if the destination field (from the config file) is in the dictionary of destination fields (in the output feature class)
                                                   ## and if the source field (from the config file) is in the dictionary of source fields in the input feature class
                dfldType = destDict[dfldUpper][0]  ## get the field type
                dfldLen = destDict[dfldUpper][1]   ## get the field length
                sfldType = srcDict[sfld][0]        ## get the field type
                sfldLen = srcDict[sfld][1]         ## get the field length
                if dfldType == 'String' and sfldType == 'String' and dfldLen < sfldLen:  ## a fatal error: field won't append
                    error += "String field length mismatch (fatal error):  target " + dfldUpper + " length: " + str(dfldLen) + " source " + sfld + " length: " + str(sfldLen) + "\n"
                if not dfldType == sfldType:           ## not a fatal error
                    message += "Field type mismatch (not a fatal error): " + dfldUpper + " (" + dfldType + ") & " + sfld + " (" + sfldType + ")\n"
    if error == "":
        return (True, message)
    else:
        return (False, error)
