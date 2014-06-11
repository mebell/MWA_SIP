import os
import sys
import mwapy.get_observation_info
from mwapy.obssched.base import schedule

# A script to retrieve a list of observations from NGAS 
# and convert them into ms files. This script will 
# then run the SIP with the settings in parset.txt

####################################################
#Parset files path(s)
loc_parset_file    = '/home/562/meb562/MWA_SIP/locs_parset.txt'
#####################################################

def read_parset(parset_file):
    """
     Read the parameter file defined in parset file path and return args
    """
    print 'Reading parameter set file'
    f = open(parset_file,'r')
    config_dict = {}
    for line in f:
        if line[0] == '#':
            pass;
        else:
            items = line.split('=', 1)
            config_dict[items[0]] = eval(items[1])
    return config_dict

####################################################
# Read the location parset to find the paths
locs = read_parset(loc_parset_file)
SIP_home = locs['SIP_home']
error_logs = locs['error_logs']
msgen_loc    = locs['msgen_loc']

####################################################

def run_obsresolve(obs_id):
    print "Getting DATA: Running obsresolve with GPS ID = "+str(obs_id)
    os.system("obsresolve.py -r ngas01.ivec.org -s ngas01.ivec.org -d ./ -o "+str(obs_id))

############## Main code ######################

obs_id = sys.argv[1] # Get the obs_id we want to work on. Parsed to the script by run_pipe.py

os.chdir(msgen_loc)
if os.path.exists(obs_id):
   print 'Data folder already made, partial download might not have completed.'
   os.chdir(obs_id)
   #run_obsresolve(obs_id)
else:
   os.mkdir(obs_id)
   os.chdir(obs_id)
   run_obsresolve(obs_id) # Get the files

# Get the metafits file
os.chdir(msgen_loc)
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
