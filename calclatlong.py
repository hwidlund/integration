#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        calclatlong.py
# Purpose:     Calculate XY/Long/Lat fields
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Date:        Feb 2016, updated Mar 25, 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
#-------------------------------------------------------------------------------

import arcpy

def CalcLatLong(inFC):

    fldNameList = [f.name for f in arcpy.ListFields(inFC,"L*","Double")]
    for fld in fldNameList:
        if fld in ["LAT", "LAT_WGS84"]:
            try:
                arcpy.CalculateField_management(inFC,fld,"!SHAPE.FIRSTPOINT.Y!", "PYTHON_9.3")
            except Exception as e:
                error = "Failed: calculate " + fld + " " + str(e)
                return (False,error)
        elif fld in ["LON", "LON_WGS84"]:
            try:
                arcpy.CalculateField_management(inFC,fld,"!SHAPE.FIRSTPOINT.X!", "PYTHON_9.3")
            except Exception as e:
                error = "Failed: calculate " + fld + " " + str(e)
                return (False,error)
        else:
            continue
    return (True,"Succeeded")