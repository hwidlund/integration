'''
Colorado West Region Data Integration Group
Name:        unzipfgdb.py
Purpose:     Unzip contents of all file geodatabases
             in a directory to a new directory
Author:      Heather Widlund, San Miguel County, CO
             heatherw@sanmiguelcountyco.gov
Created:     Apr 2016
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

 Version: Python 2.x
 Requirements:
 1. Source directory containing zip files
 2. Target directory (should not exist) where to unzip files
'''

import os, sys, shutil
import zipfile

def UnzipFgdb(srcDir,trgtDir):
    error = ""
    message = ""

    if not os.path.exists(srcDir):
        error = "Failed: unzip. " + srcDir + " does not exist."
        return (False, error)

    # delete old directory & geodatabases
    try:
        if os.path.exists(trgtDir):
            shutil.rmtree(trgtDir)
    except Exception as e:
        error = "Failed: remove {0} | {1}".format(trgtDir,str(e))
        return (False, error)
    # extract all zip files to target directory (created by extractall)
    for root,dirs,files in os.walk(srcDir):
        for filename in files:
            file = os.path.join(root,filename)  ## to obtain a file object
            if zipfile.is_zipfile(file):        ## check if is zip file
                try:
                    zf = zipfile.ZipFile(file)  ## to obtain a zip file object
                    zf.extractall(trgtDir)
                    message += "Succeeded: unzip " + filename + "\n"
                except Exception as e:
                    error += "Failed: unzip {0} | {1} \n".format(filename,(str(e)))
                    return (False, error)
                finally:
                    zf.close()
    return (True, message)