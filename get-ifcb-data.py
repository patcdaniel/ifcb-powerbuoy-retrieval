#!/bin/python3
import subprocess
import os
import paramiko
import glob
import time
import transfer


class RemoteIFCBSync:
    def __init__(self):
        self.ssh_client = self.configure_ssh()
        self.remoteBaseDir = "/mnt/data/ifcbdata/"
        self.dataFilesRemote = self.get_remote_data_files()
        self.beadFilesRemote = self.get_remote_bead_files()
        self.localBaseDir = "/opt/ifcb-data/power-buoy-deployment/"
        self.dataFilesLocal = self.get_local_data_files()
        self.beadFilesLocal = self.get_local_bead_files()

    def configure_ssh(self):
        ssh_client=paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.load_system_host_keys()
        try:
            ssh_client.connect(hostname='buoy-ifcb.shore.mbari.org', username='ifcb')
        except:
            pass # Add exception for being unable to connect
        return ssh_client
    
    def get_remote_data_files(self):
        """ Use an SSH client to 'ls' files on IFCB"""
        stdin,stdout,stderr = self.ssh_client.exec_command("ls /mnt/data/ifcbdata/*.roi")
        return sorted(stdout.readlines())

    def get_remote_bead_files(self):
        """ Use the ssh client to return a list of files in the beads directory"""
        stdin,stdout,stderr = self.ssh_client.exec_command("ls /mnt/data/ifcbdata/beads/*.roi")
        return sorted(stdout.readlines())

    def get_local_data_files(self):
        """ Use glob to get all files locally on the RAID array"""
        return glob.glob(self.localBaseDir + "*.roi")

    def get_local_bead_files(self):
        """ Use glob to get all files locally from Bead Dir on RAID array"""
        return glob.glob(os.path.join(self.localBaseDir, 'beads/')+"*.roi")

    def compare_data_files(self, beads=False):
        """Compare remote and local data files to create a list of files to be grabbed over scp"""
        if beads:
            remote_basenames = [os.path.basename(file).split(".")[0] for file in self.beadFilesRemote]
            local_basenames = [os.path.basename(file).split(".")[0] for file in self.beadFilesLocal]    

        else:
            remote_basenames = [os.path.basename(file).split(".")[0] for file in self.dataFilesRemote]
            local_basenames = [os.path.basename(file).split(".")[0] for file in self.dataFilesLocal]

        data_files_to_grab = [file for file in remote_basenames if file not in local_basenames]
        return data_files_to_grab

    def sync_files(self, beads=False):
        """ Compare the available files from remote and from local data and beads and find what files need to be transfered then copy them over via scp """

        data_files_to_copy = self.compare_data_files(beads)
        if beads:
            print("Bead files: {}".format(len(data_files_to_copy)))
        else:    
            print("Number of Data files to copy: {}".format(len(data_files_to_copy)))
        time_start = time.time() # for profiling total download time
        for fname in data_files_to_copy:
            for f_extension in [".roi",".adc",".hdr"]:
                if beads:
                    full_fname = os.path.join(self.remoteBaseDir,'beads', fname) + f_extension
                    subprocess.run(["scp",'-l','1000',"ifcb@buoy-ifcb.shore.mbari.org:"+full_fname, os.path.join(self.localBaseDir,'beads')])

                else:
                    full_fname = os.path.join(self.remoteBaseDir, fname) + f_extension
                    subprocess.run(["scp",'-l','1000',"ifcb@buoy-ifcb.shore.mbari.org:"+full_fname, self.localBaseDir]) #MegaB/Sec
                time.sleep(1) # in case the rapid grabbing of small files is causing an issues 
        time_end = time.time()
        print("Run Time (M): %2.2f " % ((time_end-time_start)//60))

    def close(self):
        self.ssh_client.close()


if __name__ == "__main__":
    remote = RemoteIFCBSync()
    remote.sync_files()
    remote.sync_files(beads=True)
    remote.close()
    transfer.transfer_files_directories() 
    subprocess.call(['sh', '/home/ifcb/bin/get-ifcb-data'])