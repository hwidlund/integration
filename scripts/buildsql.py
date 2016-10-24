#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        buildsql.py
# Purpose:     Build where clause with appropriate delimiters
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Credits:     http://gis.stackexchange.com/questions/27457/including-variable-in-where-clause-of-arcpy-select-analysis
# Date:        Jan 2016
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
def BuildSQL(inputFC, field, value):

    # Add appropriate delimiters
    fieldDelim = arcpy.AddFieldDelimiters(inputFC,field)

    # determine field type
    fieldType = arcpy.ListFields(inputFC, field)[0].type

    # Add single quotes for string types
    if str(fieldType) == 'String':
        value = "'{0}'".format(value)
    whereClause = "{0} = {1}".format(fieldDelim,value)

    return (True,whereClause)