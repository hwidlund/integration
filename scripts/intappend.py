'''
Colorado West Region Data Integration Group
Name:        intappend.py
Purpose:     Append new data into integrated dataset

Author:      Heather Widlund, San Miguel County, CO
             heatherw@sanmiguelcountyco.gov
Created:     08 May 2016
Copyright:   Heather Widlund (2016)
License:     GNU GPL
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
import os
import arcpy

def AppendToIntegrated(fgdb,intGdb):
    arcpy.env.workspace = fgdb
    outputLocation = intGdb
    newFcList = arcpy.ListFeatureClasses()
    message = ""
    for fc in newFcList:
        trgtFc = outputLocation + os.sep + fc
        if arcpy.Exists(trgtFc):
            try:
                count = int(arcpy.GetCount_management(fc).getOutput(0))
                arcpy.AddMessage("{0} | Appending {1} features".format(fc,str(count)))
                arcpy.Append_management(fc,trgtFc,"NO_TEST")
                message += "SUCCEEDED | Append " + fc
            except Exception as e:
                error = "ERROR | Append " + fc + "\n" + str(e)
                return (False, error)
    return (True, message)