'''
Colorado West Region Data Integration Group
Name:       tool_checksnaps.py
Purpose:    Script tool to check if lines near snap points are actually snapped to them.
            Create a new feature class of points where 1 or more nearby
            lines are not snapped to the point.
Requirements:
            0. Feature class containing snap points in projected coordinates
            1. Feature class containing roads in projected coordinates.
            2. New output feature class for unsnapped points
            3. Search distance (15 feet seems to work)

Author:      Heather Widlund
             heatherw@sanmiguelcountyco.gov
Created:     21 Jun 2016
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

arcpy.env.overwriteOutput = True

snapPoints = arcpy.GetParameterAsText(0)
roadLines = arcpy.GetParameterAsText(1)
outFc = arcpy.GetParameterAsText(2)
searchDistance = arcpy.GetParameterAsText(3)

try:
    # empty list which will contain the ids of the snap points which
    # are disjoint (don't share geometry) with one or more nearby lines
    ids = []

    # get the name of the object id/oid field
    oidField = arcpy.Describe(snapPoints).OIDFieldName

    # make first feature layer from snap points
    spLyr = "spLyr"
    arcpy.MakeFeatureLayer_management(snapPoints,spLyr)
    # make second feature layer from snap points
    spLyr2 = "spLyr2"
    arcpy.MakeFeatureLayer_management(snapPoints,spLyr2)
    # make road feature layer from integrated roads
    rdLyr = "rdLyr"
    arcpy.MakeFeatureLayer_management(roadLines,rdLyr)
    # iterate through snap points
    with arcpy.da.SearchCursor(snapPoints,["OID@","SHAPE@"]) as cursor:
        for row in cursor:
            # set the expression to use for selecting the current snap point feature using its oid
            exp = "{0} = {1}".format(oidField,row[0])
            # create a geometry object from the shape of the snap point
            ptGeom = row[1]
            # select the current snap point in the cursor by id
            currentSnap = arcpy.SelectLayerByAttribute_management(spLyr,"NEW_SELECTION",exp)
            # make a feature layer from the current snap point
            currentLyr = "currentLyr"
            arcpy.MakeFeatureLayer_management(currentSnap,currentLyr)
            # select the roads from the roads feature layer which are within search distance
            # of the current snap point (feature layer)
            nearbyRoads = arcpy.SelectLayerByLocation_management(rdLyr,"WITHIN_A_DISTANCE",currentLyr,searchDistance,"NEW_SELECTION")
            count = int(arcpy.GetCount_management(nearbyRoads)[0])
            if count > 0:
                # create a temporary geometry object of the selected line features
                lnGeom = arcpy.CopyFeatures_management(nearbyRoads,arcpy.Geometry())
                # iterate through line features and check if they are "disjoint" from the current
                # snap point geometry object
                for ln in lnGeom:
                    # get the endpoints of the current line
                    fpLn = ln.firstPoint
                    lpLn = ln.lastPoint
                    if ptGeom.disjoint(fpLn) and ptGeom.disjoint(lpLn):
                        # if both endpoints are disjoint(true), add this snap feature's id
                        # to the list of unsnapped
                        ids.append(row[0])
                        # add the current snap point to the second feature layer
                        # in preparation for exporting to new feature class of unsnapped points
                        arcpy.SelectLayerByAttribute_management(spLyr2,"ADD_TO_SELECTION",exp)
    arcpy.AddMessage("Unsnapped: " + str(len(ids)))
    if len(ids) != 0:
        arcpy.CopyFeatures_management(spLyr2,outFc)
        arcpy.AddMessage("Script finished. To view unsnapped, add {0} to map.".format(outFc))
    del row, cursor, currentLyr, rdLyr, spLyr, spLyr2
except Exception as e:
    arcpy.AddError("Error: " + str(e))
    arcpy.AddError(arcpy.GetMessages())