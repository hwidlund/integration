#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        configesns.py
# Purpose:     Write configuration file for Emergency Service Numbers/Zones
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Credits:     Portions adapted from Esri Community Addresses local Government Solution scripts
#              (http://solutions.arcgis.com/local-government/help/community-addresses/get-started/)
# Date:        Feb 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
#-------------------------------------------------------------------------------
# Parameters:
# 0. Output config (*.ini) file path and name
# 1. Existing feature class with updated data
# 2. Existing target file geodatabase, containing #3
# 3. Existing feature class, named ESNs,
#    with old data, target schema & spatial reference (gcs_wgs84)
# 4. Source of data, such as MONTCI, MONTCO, SANMCO, GUNNCO, DELTCO etc.
# 5. Additional SQL parameters for querying #1 in appropriate delimiter format
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

         sod = "",                          #7 SOD source of data
         sid = "",                          #8 SID unique ID
         esn = "",                          #9 ESN
         rtgesn = "",                       #10 Routing ESN
         psap = "",                         #11 PSAP name
         community = "",                    #12 Community
         law = "",                          #13 Law agency code
         fire = "",                         #14 Fire agency code
         ems = "",                          #15 EMS agency code
         splaw = "",                        #16 Law Spillman code
         spfd = "",                         #17 Fire Spillman code
         spems = "",                        #18 EMS Spillman code

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
                'EDT',
                'ESN',
                'RTG_ESN',
                'PSAP',
                'COMMUNITY',
                'LAW',
                'FIRE',
                'EMS',
                'SPLAW',
                'SPFD',
                'SPEMS']

    p_vals = [  sod,
                edt,
                esn,
                rtgesn,
                psap,
                community,
                law,
                fire,
                ems,
                splaw,
                spfd,
                spems
                ]

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
