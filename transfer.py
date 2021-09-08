#!/bin/python3
"""
Organize IFCB files into a standard structure:
/CA-IFCB-161/2021/D20210815/{FILES} -
"""

import os, glob, re, shutil, subprocess

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

    formatted_data = [os.path.basename(f) for f in sorted(glob.glob(DES_Path+"/*/*/*.*"))] # All files already transfered

    for fname in sorted(glob.glob(DATA_PATH+"*.*")):
        if not fname in formatted_data:
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
                try:
                    shutil.copy(fname, os.path.join(DES_Path,year,unique_day,base_name))

                except OSError as e:
                    # File didn't transfer completely. Try to grab it again.
                    subprocess.run(["scp",'-l','1000',"ifcb@buoy-ifcb.shore.mbari.org:/mnt/data/ifcbdata/"+fname, DATA_PATH]) #MegaB/Sec
                    shutil.copy(os.path.join(DATA_PATH ,fname), os.path.join(DES_Path,year,unique_day,fname))                    


if __name__ == "__main__":
    transfer_files_directories()