"""
Convert multiple .gpx files to shapefiles, then append them all into one shapefile.
"""

import arcpy
import os
import sys

root_dir = r"U:\Workspace\Meridian\Data\GPS_Data_20181117"
gar_dir = os.path.join(root_dir, "Garmin")
scratch_dir = os.path.join(root_dir, "scratch.gdb")

in_gpx = ""
out_fc = ""


# if scratch already exists, skip.
if not arcpy.Exists(scratch_dir):

    # create temp scratch.gdb for intermediate files, delete upon completion
    arcpy.CreateFileGDB_management(root_dir, "scratch.gdb")

    print "{} created...".format(scratch_dir)

# iterate through all files in root directory
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        in_file_path = os.path.join(subdir, file)

        # if .gpx, convert to feature class
        if in_file_path[-4:] == ".gpx":
            print file
            out_file_name = file.replace(".gpx", "")
            out_file_path = os.path.join(scratch_dir, out_file_name)

            try:
                arcpy.GPXtoFeatures_conversion(in_file_path, out_file_path)

            except Exception:
                e = sys.exc_info()[1]
                print e.args[0]
                exit(1)

            # check if file already exists in scratch, if it does, delete and replace

            if arcpy.Exists(out_file_path):
                arcpy.Delete_management(out_file_path)
                arcpy.GPXtoFeatures_conversion(in_file_path, out_file_path)

            else:
                arcpy.GPXtoFeatures_conversion(in_file_path, out_file_path)

            print "{} has been converted to feature class...".format(file)
