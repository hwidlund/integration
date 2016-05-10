#-------------------------------------------------------------------------------
# Colorado West Region Data Integration Group
# Name:        uniqueid.py
# Purpose:     Validate and check for unique IDs in SID field.
#
# Author:      Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
#
# Created:     Jan 2016, revised Mar 26, 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
#-------------------------------------------------------------------------------
# Requirements:
# 0. Input feature class to be checked for unique ids
# 1. Unique Id field name (SID in integration schema)
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

def UniqueId(inputFC, idFieldName):

    invIdList = []
    dupeIdList = []
    uniqueIdList = []
    message = ""

    try:
        rows = arcpy.da.SearchCursor(inputFC,[idFieldName])
        for row in rows:
            sid = row[0]
            if len(sid) < 8:
                invIdList.append(sid)
                continue
            if sid in uniqueIdList:
                dupeIdList.append(sid)
            else:
                uniqueIdList.append(sid)

        if len(invIdList) > 0:
            message = 'Invalid or null ids found (' + str(len(invIdList)) + ')\n'
            #message += ','.join(invIdList)
        if len(dupeIdList) > 0:
            message += 'Duplicate ids found (' + str(len(dupeIdList)) + ')\n'
            message += '\n'.join(dupeIdList)
        return (True, message)
    except Exception as e:
        error = 'Failed: validate ids. ' + str(e)
        return (False, error)