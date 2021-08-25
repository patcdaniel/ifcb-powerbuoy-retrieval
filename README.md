# MBARI IFCB 161 - Power Buoy Deployment
A collection of scripts to pull, organize and push IFCB data from the Power Buoy to the Axiom IFCB Dashboard.
<br>

Files:

    get-ifcb-data - Bash script that sets permissions, organizes files on the RAID array (/opt/ifcb-data/power-buoy-deployment) then pushes the data to Axiom data science using rsync. The public SSH key for this account (ifcb@particle) was sent to them, so no other authorization is needed - This is run at the end of the get-ifcb-data.py
    get-ifcb-data.py - Python scipt that uses SSH to check what files are on the IFCB and then checks them against the files on the RAID array. The difference in files are then downloaded off the of the instrument using scp with the bandwidth limited to 125KBytes/sec (1000Kbits/sec). __This is key!!__. This script is currenly run every 2 hours on CRON: `0 */2 * * * python3 /home/ifcb/bin/get-ifcb-data.py`
    transfer.py - Python script that organzies and copies files into a standard directory format. This is to help ingestion into the IFCB dashboard. This is run at the end of the get-ifcb-data.py script.
<br>

ALSO: please update the email and name for git on particle
