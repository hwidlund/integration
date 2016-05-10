#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        truncate_table.py
# Purpose:     Delete all old records in output feature class to prepare
#              for appending of updated records
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Date:        Jan 2016, updated Mar 25, 2016
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
def Truncate(outputFC):

    # Delete all data in output feature class
    try:
        arcpy.TruncateTable_management(outputFC)
        return (True, 'Succeeded')
    except Exception as e:
        error = "Failed: truncate output feature class table. " + str(e)
        return (False, error)