'''
Colorado West Region Data Integration Group
Name:       intsodlist.py
Purpose:    create list of valid agency code (SOD) values for each feature class, add to
            a dictionary with the key as the feature class name, and the list as the value
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
def GetUniqueSods(fgdb, sodField):
    arcpy.env.workspace = fgdb
    # get root of fgdb, which will be the name of the agency
    fgdbName = os.path.basename(os.path.splitext(fgdb)[0])
    fgdbDict = {}
    # add all the feature classes to a list
    fcList = arcpy.ListFeatureClasses()

    # loop through fc in list
    for fc in fcList:
        uniqueList = []
        # if the SOD field is in the list of fields for the feature class,
        # (list obtained with list comprehension)
        # cycle through values in SOD field and create a list of unique values
        try:
            if sodField in [f.name for f in arcpy.ListFields(fc,"",sodField)]:
                with arcpy.da.SearchCursor(fc,sodField) as cursor:
                    for row in cursor:
                        if not row[0] in uniqueList:
                            uniqueList.append(row[0])
                del row, cursor
                # add to dictionary of key:value pairs where fc is the key and the list of values is the value
                fgdbDict[fc] = [uniqueList]
        except Exception as e:
            error = "ERROR | {0} {1} : Create unique list of SOD values- {2}".format(fgdbName,fc, str(e))
            return(False,error)
    return(True,fgdbDict)