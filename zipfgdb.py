#-------------------------------------------------------------------------------
# Name:        zipfgdb.py
# Purpose:     Zip file geodatabase
# Contact:     Heather Widlund, San Miguel County, CO
#              heatherw@sanmiguelcountyco.gov
# Date:        Feb 2016, revised Mar 25, 2016
# Versions:    Python 2.7.5 & ArcGIS 10.2+
# Credits:     Adapted from http://www.maprantala.com/2011/02/08/zipping-a-file-geodatabase-using-python/
#-------------------------------------------------------------------------------
# Requirements
# 0. Full path to output data directory where fgdb lives
#-------------------------------------------------------------------------------
import os, sys
import glob
import zipfile

def ZipFgdb(dataPath):
    error = ""
    # check for existence
    if not (os.path.exists(dataPath)):
        error = "Failed: " + dataPath + " not found. Exiting."
        return (False, error)

    for root,dirs,files in os.walk(dataPath):
        for dir in dirs:
            if str(dir).endswith('.gdb'):
                fgdb = os.path.join(dataPath, str(dir))
                # make the zip file name the same as the fgdb name - i.e. SOD code
                zipFileName = (os.path.splitext(fgdb)[0]) + ".zip"
                if (os.path.exists(zipFileName)):
                    os.remove(zipFileName)
                try:
                    zipHandle = zipfile.ZipFile(zipFileName,'w')
                    for f in glob.glob(fgdb + os.sep + "*"):
                        if not str(f).endswith('lock'):
                            zipHandle.write(f, os.path.basename(fgdb) + os.sep + os.path.basename(f), zipfile.ZIP_DEFLATED)
                except Exception as e:
                    error += "Failed: zip geodatabase " + str(zipFileName) + "\n" + str(e) + "\n"
                finally:
                    zipHandle.close()
    if not error == "":
        return (False,error)
    else:
        return (True, "Succeeded")

if __name__ == '__main__':
    ZipFgdb(sys.argv[1])