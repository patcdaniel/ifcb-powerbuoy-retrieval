#!/bin/python3
"""
Organize IFCB files into a standard structure:
/CA-IFCB-161/2021/D20210815/{FILES} -
"""

import os, glob, re, shutil

# GLOBALS
DATA_PATH = "/opt/ifcb-data/power-buoy-deployment/"
DES_Path = os.path.join(DATA_PATH,"CA-IFCB-161")

def transfer_files_directories():
    """
    Search all file names, create a file directory for each year and a subdirectory of each month,if
    either doesn't already exists, then move files into that directory.
    Assume that there are .hdr, .roi, and .adc files for each filename
    Example structure /CA-IFCB-161/2021/D20210718/
    """
    for fname in sorted(glob.glob(DATA_PATH+"*.hdr")):
        pattern = r"(D(\d\d\d\d)(\d\d\d\d))"
        base_name = os.path.basename(fname)
        date_str = re.findall(pattern, base_name)

        if bool(date_str):
            year = date_str[0][1]
            unique_day = date_str[0][0]

            if not os.path.isdir(os.path.join(DES_Path,year)):
                oldmask = os.umask(000)
                os.makedirs(os.path.join(DES_Path,year,unique_day), 0o777)
                os.umask(oldmask)
            
            else:
                if not os.path.isdir(os.path.join(DES_Path,year,unique_day)):
                    oldmask = os.umask(000)
                    os.mkdir(os.path.join(DES_Path,year,unique_day), 0o775)
                    os.umask(oldmask)
            
            shutil.copy(fname, os.path.join(DES_Path,year,unique_day,base_name))
            shutil.copy(os.path.join(DATA_PATH, base_name.split('.')[0]) + ".roi", os.path.join(DES_Path,year,unique_day,base_name.split('.')[0] + ".roi"))
            shutil.copy(os.path.join(DATA_PATH ,base_name.split('.')[0]) + ".adc", os.path.join(DES_Path,year,unique_day,base_name.split('.')[0] + ".adc"))


if __name__ == "__main__":
    transfer_files_directories()