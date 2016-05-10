#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        config_placenamepts.py
# Purpose:     Write configuration file for place name points
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Credits:     Portions adapted from Esri Community Addresses local Government Solution scripts
#              (http://solutions.arcgis.com/local-government/help/community-addresses/get-started/)
# Date:        Jan 2016; formatting updated Apr 10, 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
#-------------------------------------------------------------------------------
# Parameters:
# 0. Output config (*.ini) file path and name
# 1. Existing feature class with updated data
# 2. Existing target file geodatabase, containing #3
# 3. Existing feature class with old data, target schema & spatial reference (gcs_wgs84)
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

def main(config_file,                       # config file name & path
         inputFeatureClass = "",            # fc with updated data & local schema
         outputFileGdb = "",                # output file geodatabase
         outputFeatureClass = "",           # existing fc with target schema

         srcOfData = "",                    # SOD for where clause, such as: SANMCO, MONTCO, etc.
         addlSql = "",                      # additional SQL where clause parameters
                                            # ex. OR SOD = 'SANJCO' OR SOD = 'HINSCO'

         datumTransformation = "",          # Datum Transformation

         sodCode = "",                      # SOD (for field mapping)
         stateId = "",                      # STATE_ID
         uniqueSiteId = "",                 # SID
         dateLastUpdated = "",              # DLU
         name = "",                         # NAME
         alias = "",                        # ALIAS
         alias2 = "",                       # ALIAS2
         siteAddressNumber = "",            # SAN
         siteAddressNumberSuffix = "",      # SNS
         streetPrefixDirection = "",        # PRD
         streetPrefixType = "",             # PRT
         streetName = "",                   # RD
         streetTypeSuffix = "",             # STS
         streetPostDirection = "",          # POD
         unitDesignation = "",              # UNIT
         fullSiteAddress = "",              # FSA
         spillmanSA = "",                   # SPSA
         postalCommunity = "",              # PCN
         msagCommunity = "",                # MCN
         zipCode = "",                      # ZIP
         countyName = "",                   # COUNTY
         countyFips = "",                   # COUNTYFIPS
         state = "",                        # STA
         gnisId = "",                       # GNIS_ID
         cla = "",                          # CLASS
         subClass = "",                     # SUBCLASS
         subClass2 = "",                    # SUBCLASS2
         naics = "",                        # NAICS
         steward = "",                      # STEWARD
         source = "",                       # SOURCE
         sourceQc = "",                     # SOURCE_QC
         collection = "",                   # COLLECTION
         uploadDate = "",                   # UPLOADDATE
         quality = "",                      # QUALITY
         latitude = "",                     # LAT_WGS84
         longitude = "",                    # LON_WGS84
         elAppxFt = "",                     # EL_APPX_FT
         facilityContact = "",              # FACILITY_C
         contactPhone = "",                 # CONTACT_PH
         publicPhone = "",                  # PUBLIC_PH
         comments = "",                     # COMMENTS
         publicYN = "",                     # PUB
         essFacility = "",                  # ESSFAC
         commAnchInst = "",                 # CAI
        *args):
    config = ConfigParser.RawConfigParser()
    arcpy.AddMessage('Configuration file created')

    #-------------------------
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

    #-------------------------
    # SQL parameters
    section = 'SQL_PARAMETERS'
    p_names = ['SOURCE','ADDLSQL']
    p_vals = [ srcOfData, addlSql ]

    arcpy.AddMessage('Writing SQL parameters...')
    write_config(p_names,p_vals,config,section)

    # -------------------------
    # Spatial Reference parameter
    section = 'SPATIAL_REF'
    p_names = [ 'DATUMTRANS']
    p_vals = [ datumTransformation ]

    arcpy.AddMessage('Writing spatial reference parameter...')
    write_config(p_names,p_vals,config,section)

    # ------------------------
    # Field mapping parameters
    # keys (p_names) must match field names in target schema feature class
    section = 'FIELD_MAPPER'
    p_names = [ 'SOD',
                'STATE_ID',
                'SID',
                'DLU',
                'NAME',
                'ALIAS',
                'ALIAS2',
                'SAN',
                'SNS',
                'PRD',
                'PRT',
                'RD',
                'STS',
                'POD',
                'UNIT',
                'FSA',
                'SPSA',
                'PCN',
                'MCN',
                'ZIP',
                'COUNTY',
                'COUNTYFIPS',
                'STA',
                'GNIS_ID',
                'CLASS',
                'SUBCLASS',
                'SUBCLASS2',
                'NAICS',
                'STEWARD',
                'SOURCE',
                'SOURCE_QC',
                'COLLECTION',
                'UPLOADDATE',
                'QUALITY',
                'LAT_WGS84',
                'LON_WGS84',
                'EL_APPX_FT',
                'FACILITY_C',
                'CONTACT_PH',
                'PUBLIC_PH',
                'COMMENTS',
                'PUB',
                'ESSFAC',
                'CAI']

    p_vals = [  sodCode,
                stateId,
                uniqueSiteId,
                dateLastUpdated,
                name,
                alias,
                alias2,
                siteAddressNumber,
                siteAddressNumberSuffix,
                streetPrefixDirection,
                streetPrefixType,
                streetName,
                streetTypeSuffix,
                streetPostDirection,
                unitDesignation,
                fullSiteAddress,
                spillmanSA,
                postalCommunity,
                msagCommunity,
                zipCode,
                countyName,
                countyFips,
                state,
                gnisId,
                cla,
                subClass,
                subClass2,
                naics,
                steward,
                source,
                sourceQc,
                collection,
                uploadDate,
                quality,
                latitude,
                longitude,
                elAppxFt,
                facilityContact,
                contactPhone,
                publicPhone,
                comments,
                publicYN,
                essFacility,
                commAnchInst ]

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
