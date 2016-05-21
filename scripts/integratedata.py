'''
Colorado West Region Data Integration Group
Name:       integratedata.py
Purpose:    integrate data from zipped file geodatabases using SCRIPT TOOL

Author:      Heather Widlund, San Miguel County, CO
             heatherw@sanmiguelcountyco.gov
Created:     08 May 2016, updated 5/21/16
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
import os, sys
import arcpy
import intunzipfgdb         ## unzip databases
import intsodlist           ## create dictionary of valid SOD values for each layer
import intdeletedata        ## delete old data using SOD list
import intappend            ## append new data
import removemetadata       ## remove gp history & machine info

def IntegrateData(srcDir, trgtDir, integratedGdb):
    arcpy.env.overwriteOutput = True
    arcpy.AddMessage("Starting data integration...")
    arcpy.AddMessage("Unzipping geodatabases from " + srcDir)

    # unzip all file geodatabases to a directory
    result = intunzipfgdb.UnzipFgdb(srcDir, trgtDir)
    if not result[0]:
        error = "Failed: unzip geodatabases. | " + result[1]
        arcpy.AddError(error)
        sys.exit(1)
    arcpy.AddMessage("Succeeded: unzip geodatabases.")
    # list all the file geodatabases in the target directory
    arcpy.env.workspace = trgtDir
    fgdbNames = arcpy.ListWorkspaces("*","FileGDB")
    sodField = "SOD"        ## source of data field

    # loop through file geodatabases
    # for each geodatabase:
        # create where clauses for deleting old data
        # delete old data
        # append new data
        #remove metadata (gp history and machine info)
    for fgdb in fgdbNames:
        arcpy.env.workspace = fgdb
        agencyName = os.path.basename(os.path.splitext(fgdb)[0])

        # get dictionary of {layer names:unique sods}
        arcpy.AddMessage(agencyName + ": getting list of unique SOD values...")
        result = intsodlist.GetUniqueSods(fgdb, sodField)
        if not result[0]:
            error = "{0} | Failed: get unique SOD values. | {1}".format(agencyName, result[1])
            arcpy.AddError(error)
            sys.exit(2)
        wcDict = result[1]
        arcpy.AddMessage(agencyName + " | Succeeded: get unique SOD values.")

        # delete old data using where clause of unique sod values
        arcpy.AddMessage(agencyName + ": deleting old data from integrated gdb...")
        result = intdeletedata.DeleteData(integratedGdb, wcDict)
        if not result[0]:
            error = "{0} | Failed: delete old data | {1}".format(agencyName, result[1])
            arcpy.AddError(error)
            sys.exit(3)
        arcpy.AddMessage(agencyName + " | Succeeded: delete old data.")

        arcpy.AddMessage(agencyName + ": appending new data...")

        # append features into integrated
        result = intappend.AppendToIntegrated(fgdb,integratedGdb)
        if not result[0]:
            error = "{0} | Failed: append new data | {1}".format(agencyName, result[1])
            arcpy.AddError(error)
            sys.exit(4)
        arcpy.AddMessage(agencyName + " | Succeeded: append new data.")
    arcpy.AddMessage("Succeeded: integrate data.")

    # iterate through each feature class in the integrated file geodatabase and remove unwanted metadata
    arcpy.env.workspace = integratedGdb
    newFcList = arcpy.ListFeatureClasses()
    arcpy.AddMessage("Removing unneeded metadata from " + integratedGdb)
    for fc in newFcList:
        result = removemetadata.RemoveUnwantedMetadata(integratedGdb,fc)
        if not result[0]:
            error = "{0}: {1} | Failed: remove unneeded metadata | {2}".format(integratedGdb, fc, result[1])
            arcpy.AddError(error)
            sys.exit(5)
    arcpy.AddMessage(integratedGdb + " | Succeeded: remove unneeded metadata.")
    # end of the loop for the file geodatabase



if __name__ == "__main__":
    srcDir = arcpy.GetParameterAsText(0)
    trgtDir = arcpy.GetParameterAsText(1)
    intGdb = arcpy.GetParameterAsText(2)
    IntegrateData(srcDir,trgtDir,intGdb)