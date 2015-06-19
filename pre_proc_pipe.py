import os
import sys

# A script to run cotter then CASA. This must be in a 
# different script to the download becuase we use different
# ques to submit the qsub commands. Download = copq which uses node
# that can see the outside world, but are limited in number. Normal 
# que will only used compute nodes, with no outside access. The download
# is run on the copy que nodes and tis script is run on the normal nodes.  

####################################################
#Parset files path(s)
loc_parset_file    = '/home/562/meb562/MWA_SIP/locs_parset.txt'
parset_file    = '/home/562/meb562/MWA_SIP/parset.txt'
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

def run_cotter(obs_id):
    #os.system('make_metafits.py --gps='+str(obs_id))
    os.system('cotter -o '+str(obs_id)+'.ms -mem 75 -timeres 2 -freqres 80 -m '+str(obs_id)+'.metafits '+str(obs_id)+'/*.fits')

####################################################
# Read the location parset to find the paths
locs = read_parset(loc_parset_file)
SIP_home = locs['SIP_home']
error_logs = locs['error_logs']
msgen_loc    = locs['msgen_loc']
results_dir = locs['results_dir']
OBS_ID_LIST = open(SIP_home+'/obs_id_list.txt', 'r')

############## Main code ######################

obs_id = sys.argv[1] # Get the obs_id we want to work on. Parsed to the script by run_pipe.py
os.chdir(msgen_loc)
os.chdir(obs_id)

if os.path.exists(str(obs_id)+'.ms'):
   print 'Data already pre-processed, skipping'
else:   
   run_cotter(obs_id)
   os.system('rm -rf '+str(obs_id))

uvfits_dir = os.getcwd()

######## Find a calibrator ##########
parset = read_parset(parset_file)
do_parset_cal = parset['do_parset_cal']

if do_parset_cal:
        cal = locs['cal_loc']
else:
        # Get the autocal selection and parse it to the CASA script
	f = open('cal.txt')
	lines = f.readlines()
	cal = lines[0]
	f.close()
	if cal is None:
	       print "Exiting no calibrator found"  
	       os._exit(1)

######### Run the CASA pipe ##########
file_to_process = (str(uvfits_dir)+'/'+str(obs_id)+".ms") 
print 'Created '+file_to_process+' : parsing to CASA for reduction' 
os.system("/short/ek6/CASA/casapy-stable-42.0.26465-001-64b/casapy -c "+SIP_home+"/SIP_128T_parallel_phase_3.py  "+file_to_process+' '+cal)
# Copy all the images to results dir. 
os.system('cp *_I.fits '+results_dir)
os.system('cp *_XX.fits '+results_dir)
os.system('cp *_YY.fits '+results_dir)
os.system('cp *_Q.fits '+results_dir)
os.system('cp *_U.fits '+results_dir)
os.system('cp *_V.fits '+results_dir)
# Remove the raw data (optional see parset)

doRemove = parset['doRemove']

if doRemove:
   os.system('rm -rf '+str(msgen_loc)+'/'+str(obs_id))     
