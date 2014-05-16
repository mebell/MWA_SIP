import os
import sys
import mwapy.get_observation_info
from mwapy.obssched.base import schedule

# A script to retrieve a list of observations from NGAS 
# and convert them into ms files. This script will 
# then run the SIP with the settings in parset.txt

################ Configs ####################
OBS_ID_LIST = '/home/562/meb562/SIP/obs_id_list.txt' # This contains the GPS IDs of the observations you want to reduce.
UVGEN_LOC    = '/short/ek6/meb562/tmp_data/'
##############################################

def run_obsresolve(obs_id):
    print "Getting DATA: Running obsresolve with GPS ID = "+str(obs_id)
    os.system("obsresolve.py -t 8 -r ngas01.ivec.org -s ngas01.ivec.org -d ./ -o "+str(obs_id))

############## Main code ######################

obs_id = sys.argv[1] # Get the obs_id we want to work on. Parsed to the script by run_pipe.py

os.chdir(UVGEN_LOC)
if os.path.exists(obs_id):
   print 'Data folder already made, partial download might not have completed.'
   os.chdir(obs_id)
   #run_obsresolve(obs_id)
else:
   os.mkdir(obs_id)
   os.chdir(obs_id)
   run_obsresolve(obs_id) # Get the files

# Get the metafits file
os.chdir(UVGEN_LOC)
os.chdir(obs_id)
os.system('make_metafits.py --gps='+str(obs_id))
############# Delays #################
# Get the delays while we are on a copyq node
db=schedule.getdb()
info=mwapy.get_observation_info.MWA_Observation(obs_id,db=db)
delays=info.delays
str_delays=','.join(map(str,delays))
print "Getting observation delays, writing to file"
file = open("delays.txt", "w")
file.write(str_delays)
file.close()
