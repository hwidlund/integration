#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        removemetadata.py
# Purpose:     Remove geoprocessing history and local storage info from all
#              feature classes in a geodatabase
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Date:        Feb 2016, revised Mar 25, 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
# Sources:
# get install directory: http://resources.arcgis.com/en/help/main/10.2/index.html#/GetInstallInfo/03q300000006000000/
# do the xsl transform: http://support.esri.com/de/knowledgebase/techarticles/detail/41026
#-------------------------------------------------------------------------------
# Requirements
# 0. Input file geodatabase
# 1. Input feature class
#-------------------------------------------------------------------------------

import os, sys, shutil
import arcpy

def RemoveUnwantedMetadata(fgdb, fc):

    # set environments & variables
    arcpy.env.workspace = fgdb
    # the full path of feature class is passed, and we need the base name
    featureClass = os.path.basename(fc)
    # the below construction makes it installation independent
    installDir = arcpy.GetInstallInfo()['InstallDir']
    ssPath1 = 'Metadata\\Stylesheets\\gpTools\\remove geoprocessing history.xslt'
    ssPath2 = 'Metadata\\Stylesheets\\gpTools\\remove local storage info.xslt'

    xsltPath1 = installDir + ssPath1
    xsltPath2 = installDir + ssPath2

    # delete the output directory if it already exists so you don't have to overwrite
    outXml = 'c:\\XML_out'
    if os.path.exists(outXml):
        shutil.rmtree(outXml)
    os.mkdir(outXml)

    # Remove geoprocessing history and local machine name/paths

    # output xml for removing gp history
    nameXml1 = outXml + os.sep + str(featureClass) + ".xml"
    # output xml for removing local storage info
    nameXml2 = outXml + os.sep + str(featureClass) + "2.xml"

    try:
        arcpy.XSLTransform_conversion(featureClass, xsltPath1, nameXml1,"")
        arcpy.MetadataImporter_conversion(nameXml1, featureClass)
        arcpy.XSLTransform_conversion(featureClass, xsltPath2, nameXml2,"")
        arcpy.MetadataImporter_conversion(nameXml2, featureClass)
        return (True,"Succeeded")
    except Exception as e:
        error = "Failed: metadata removal for " + str(fc) + " " + str(e)
        return (False,error)
    finally:
        # clean up
        shutil.rmtree(outXml)
