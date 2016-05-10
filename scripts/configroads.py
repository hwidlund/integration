#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        config_roads.py
# Purpose:     Write configuration file for road centerlines
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Credits:     Portions adapted from Esri Community Addresses local Government Solution scripts
#              (http://solutions.arcgis.com/local-government/help/community-addresses/get-started/)
# Date:        Jan 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
#-------------------------------------------------------------------------------
# Parameters:
# 0. Output config (*.ini) file path and name
# 1. Existing feature class with updated data
# 2. Existing target file geodatabase, containing #3
# 3. Existing feature class, named <SOD>_ROADS,
#    with old data, target schema & spatial reference (gcs_wgs84)
# 4. Source of data, such as MONTCI, MONTCO, SANMCO, GUNNCO, DELTCO etc.
# 5. Additional SQL parameters for querying #1 in appropriate format
#      for source data such as OR SOD = 'HINSCO' or AND "MCN" = 'TELLURIDE'
# Rest of parameters are for field mapping
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

from os.path import dirname, join, realpath
import arcpy
import ConfigParser

def write_config(names, vals, config, section):

    config.add_section(section)

    i=0
    while i < len(names):
        if vals[i] == "#" or vals[i] =="":
            vals[i] = ''
        config.set(section, names[i], vals[i])
        i += 1

def main(config_file,                       #0 config file name & path
         inputFeatureClass = "",            #1 fc with updated data & local schema
         outputFileGdb = "",                #2 output file geodatabase
         outputFeatureClass = "",           #3 existing fc with target schema

         srcOfData = "",                    #4 SOD for where clause, such as: SANMCO, MONTCO, etc.
         addlSql = "",                      #5 additional SQL where clause parameters
                                            # ex. OR SOD = 'SANJCO' OR SOD = 'HINSCO'

         datumTransformation = "",          #6 Datum Transformation

         sodCode = "",                      #7 SOD
         uniqueId = "",                     #8 SID
         leftFrom = "",                     #9 LFR
         leftTo = "",                       #10 LTO
         rightFrom = "",                    #11 RFR
         rightTo = "",                      #12 RTO
         streetPrefixDirection = "",        #13 PRD
         streetName = "",                   #14 RD
         streetTypeSuffix = "",             #15 STS
         streetPostDirection = "",          #16 POD
         fullStreetName = "",               #17 FSN
         aliasStreetName = "",              #18 ASN
         aliasStreetName2 = "",             #19 ASN2
         aliasStreetName3 = "",             #20 ASN3
         aliasStreetName4 = "",             #21 ASN4
         postalCommunityLeft = "",          #22 PCNL
         postalCommunityRight = "",         #23 PCNR
         msagCommunityLeft = "",            #24 MCL
         msagCommunityRight = "",           #25 MCR
         emergencyServiceNumberLeft = "",   #26 ESNL
         emergencyServiceNumberRight = "",  #27 ESNR
         roadClass = "",                    #28 ROC
         roadSubClass = "",                 #29 ROSC
         speed = "",                        #30 SPEED

         *args):
    config = ConfigParser.RawConfigParser()
    arcpy.AddMessage('Configuration file created')

    # Data parameters
    section = 'LOCAL_DATA'
    p_names = ['INPUTFC',
                'OUTPUTFGDB',
                'OUTPUTFC']

    p_vals = [ inputFeatureClass,
                outputFileGdb,
                outputFeatureClass ]

    arcpy.AddMessage('Writing data source parameters...')
    write_config(p_names,p_vals,config,section)

    # SQL parameters
    section = 'SQL_PARAMETERS'
    p_names = ['SOURCE','ADDLSQL']
    p_vals = [ srcOfData, addlSql ]

    arcpy.AddMessage('Writing SQL parameters...')
    write_config(p_names,p_vals,config,section)

    # Spatial Reference parameter
    section = 'SPATIAL_REF'
    p_names = [ 'DATUMTRANS']
    p_vals = [ datumTransformation ]

    arcpy.AddMessage('Writing spatial reference parameter...')
    write_config(p_names,p_vals,config,section)

    # Field mapping
    # keys (p_names) must match field names in target schema feature class
    section = 'FIELD_MAPPER'
    p_names = [ 'SOD',
                'SID',
                'LFR',
                'LTO',
                'RFR',
                'RTO',
                'PRD',
                'RD',
                'STS',
                'POD',
                'FSN',
                'ASN',
                'ASN2',
                'ASN3',
                'ASN4',
                'PCNL',
                'PCNR',
                'MCL',
                'MCR',
                'ESNL',
                'ESNR',
                'ROC',
                'ROSC',
                'SPEED']

    p_vals = [  sodCode,
                uniqueId,
                leftFrom,
                leftTo,
                rightFrom,
                rightTo,
                streetPrefixDirection,
                streetName,
                streetTypeSuffix,
                streetPostDirection,
                fullStreetName,
                aliasStreetName,
                aliasStreetName2,
                aliasStreetName3,
                aliasStreetName4,
                postalCommunityLeft,
                postalCommunityRight,
                msagCommunityLeft,
                msagCommunityRight,
                emergencyServiceNumberLeft,
                emergencyServiceNumberRight,
                roadClass,
                roadSubClass,
                speed ]

    arcpy.AddMessage('Writing field mapping parameters...')
    write_config(p_names,p_vals,config,section)

    cfgpath = dirname(realpath(__file__))
    cfgfile = join(cfgpath, "{}".format(config_file))

    with open(cfgfile, "w") as cfg:
        arcpy.AddMessage('Saving configuration "{}"...'.format(cfgfile))
        config.write(cfg)
    arcpy.AddMessage("Completed configuration")

if __name__ == '__main__':
    argv = tuple(arcpy.GetParameterAsText(i) for i in range(arcpy.GetArgumentCount()))
    main(*argv)
