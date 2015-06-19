import os
import sys
import mwapy.get_observation_info
from mwapy.obssched.base import schedule
from subprocess import Popen, PIPE
import glob

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

#####################################################
def find_cal(obs_id):
    obs_id = obs_id.split('\n')[0]
    obs_id = obs_id.strip()
    cal_pref = 'HydA'
    do_cal_pref = False
    if do_cal_pref:
       cal_output = Popen(["python", "/short/ek6/MWA_Code/MWA_extras/find_calibrator.py", "-v","--matchproject","--source="+cal_pref,  str(obs_id)], stdout=PIPE).communicate()[0]
    else:
       cal_output = Popen(["python", "/short/ek6/MWA_Code/MWA_extras/find_calibrator.py", "-v","--matchproject", str(obs_id)], stdout=PIPE).communicate()[0]
    try:
       cal_id = cal_output.split()[7]
       cal_name = cal_output.split()[10]
       print str(obs_id)+": recommended cal is "+str(cal_id)+' = '+str(cal_name)
    except:
       print str(obs_id)+": cannot find suitable cal "
       cal_id=None
       pass;
    os.chdir('/home/562/meb562/CALS/')
    cal_num = None
    return_cal = None
    for cal in glob.glob('*.cal'):
        cal_num = cal[0:10]
        if cal_id == cal_num:
           print "Found calibration file "+cal
           return_cal = '/home/562/meb562/CALS/'+cal
    if return_cal == None:
           print "No calibrator file found, please generate it"
    return return_cal

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

cal = find_cal(obs_id) # Look for a calibrator

if cal == None:
   print 'Error: No calibrator found, exciting processing'
   os._exit(1) 
else:
	os.chdir(msgen_loc)
	if os.path.exists(obs_id):
	   print 'Data folder already made, partial download might not have completed.'
	   os.chdir(obs_id)
	   run_obsresolve(obs_id)
	else:
	   os.mkdir(obs_id)
	   os.chdir(obs_id)
	   run_obsresolve(obs_id) # Get the files

	os.chdir(msgen_loc)
	os.chdir(obs_id)
        # Make the metafits for cotter
	os.system('make_metafits.py --gps='+str(obs_id))
        #########################
	cal_file = open("cal.txt", "w") 
	cal_file.write(str(cal))
	cal_file.close()




