from cProfile import run
import subprocess
import os
import time


def pull_sample(sample_name: str, sleep = .5):
    """ Grab the .hdr, .adc, and .roi file given a sample name """
    remoteBaseDir = "/mnt/data/ifcbdata/"
    localBaseDir = "/home/ifcb/bin/testing-file-transfer/"

    for f_extension in [".roi",".adc",".hdr"]:                
        full_fname = os.path.join(remoteBaseDir, sample_name) + f_extension
        subprocess.run(["scp",'-l','1000',"ifcb@buoy-ifcb.shore.mbari.org:"+full_fname, localBaseDir]) #kilobits/Sec == 250 kBytes/sec
        time.sleep(sleep) # in case the rapid grabbing of small files is causing an issues 

def main(run_nfiles = 4, large=False):
    """Run script, includes a list of 24 files to possibly grab. larger fnames are samples ~3-4 MB for roi which is more realistics for higher producrtivity
    """
    larger_fnames = ["D20220329T041451_IFCB161",
            "D20220405T011415_IFCB161",
            "D20220330T041326_IFCB161",
            "D20220329T034519_IFCB161",
            "D20220404T223911_IFCB161",
            "D20220405T014346_IFCB161",
            "D20220405T003720_IFCB161",
            "D20220329T030101_IFCB161",
            "D20220326T195533_IFCB161",
            "D20220329T062425_IFCB161",
            "D20220404T233052_IFCB161",
            "D20220325T195828_IFCB161",]
    
    smaller_fnames = ["D20220406T055944_IFCB161",
        "D20220406T060707_IFCB161",
        "D20220406T061429_IFCB161",
        "D20220406T062152_IFCB161",
        "D20220406T062915_IFCB161",
        "D20220406T063639_IFCB161",
        "D20220406T064402_IFCB161",
        "D20220406T065125_IFCB161",
        "D20220406T065848_IFCB161",
        "D20220406T070611_IFCB161",
        "D20220406T071334_IFCB161",
        "D20220406T072057_IFCB161",
        "D20220406T072820_IFCB161",
        "D20220406T073543_IFCB161",
        "D20220406T074306_IFCB161",
        "D20220406T075028_IFCB161",
        "D20220406T075751_IFCB161",
        "D20220406T080514_IFCB161",
        "D20220406T081237_IFCB161",
        "D20220406T082000_IFCB161",
        "D20220406T082723_IFCB161",
        "D20220406T083446_IFCB161",
        "D20220406T084209_IFCB161",
        "D20220406T084932_IFCB161"]

    if large:
        fnames = larger_fnames
    else:
        fnames = smaller_fnames

    start = time.perf_counter()
    for fname in fnames[:run_nfiles]:
        pull_sample(fname)
    finish = time.perf_counter()   
    print( f"Total Ellapsed Seconds {round(finish-start,2 )}")

if __name__ == "__main__":
    main(run_nfiles=1, large=True)