import os, sys
from subprocess import Popen, PIPE
import glob
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
SIP_home   = locs['SIP_home']
####################################################

# Work out which GPS ID / datafile we are going to work on
id_file = open(SIP_home+'/obs_id_list.txt', 'r')
#id_file = open(SIP_home+'/files_to_process/all_0953.txt', 'r')

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
           return_cal = cal_id
    if return_cal == None: 
           print "No calibrator file found, please generate it"
           return_cal = cal_id
    return return_cal
        
get_cals = []
count = 1
for line in id_file:
    print count
    return_cal = find_cal(line)
    if return_cal == None:
       pass;
    else:
       if return_cal not in get_cals:
          get_cals.append(return_cal)
    count = count + 1 

print "Get these cals"
for cal in get_cals:
    print cal





