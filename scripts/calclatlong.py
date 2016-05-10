#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        calclatlong.py
# Purpose:     Calculate XY/Long/Lat fields
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Date:        Feb 2016, updated Mar 25, 2016
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