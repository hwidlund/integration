'''
Name:        intdeletedata.py
Purpose:     Delete old data from integrated dataset, using where clause
             constructed from the unique SODs that exist in the incoming data
Requirements:
            1. Integrated geodatabase to delete data from
            2. Dictionary of {feature class name: [valid agency codes]}
            passed from integratedata.py
            3. A field in the integrated data corresponding to agency code
Author:      Heather Widlund, San Miguel County, CO
             heatherw@sanmiguelcountyco.gov
Created:     08 May 2016, Revised 24 Sept 2016 to delete by OID instead of SID
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
import arcpy

def CreateWhereClause(validSodList, sodField):
    whereClause = ""
    for sod in validSodList:
        whereClause += "{0}='{1}' OR ".format(sodField,sod)
    endSlice = len(whereClause)-4                   ## chop off final "or"
    whereClause = whereClause[:endSlice]
    return(True, whereClause)

def DeleteData(intGdb, wcDict, sodField):
    # set workspace to integrated geodatabase
    arcpy.env.workspace = intGdb
    arcpy.env.overwriteOutput = True
    # list feature classes in integrated geodatabase
    intFcList = arcpy.ListFeatureClasses()
    # loop through feature classes and delete old data
    for fc in intFcList:
        if fc in wcDict:
            # look for feature class name as key in dictionary
            # grab valid list of sods from value element
            validSodList = wcDict[fc][0]
            result = CreateWhereClause(validSodList, sodField)  ## call above function to create the list
            whereClause = result[1]
            fcLyr = "fcLyr"
            try:
                arcpy.MakeFeatureLayer_management(fc,fcLyr,whereClause)
                arcpy.SelectLayerByAttribute_management(fcLyr,"NEW_SELECTION",whereClause)
                count = int(arcpy.GetCount_management(fcLyr).getOutput(0))
                if count > 0:
                    i = 0
                    with arcpy.da.UpdateCursor(fcLyr,["OID@"]) as cursor:
                        for row in cursor:
                            i+= 1
                            cursor.deleteRow()
                    arcpy.AddMessage("{0} | Succeeded: deleted {1} features".format(fc,str(i)))
            except Exception as e:
                error = "ERROR | Delete {0} /n {1}".format(fc,str(e))
                return (False, error)
            finally:
                del fcLyr
    return(True, "Succeeded")