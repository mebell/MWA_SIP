import os
import sys
import pyfits
import glob
import commands
from astropy import units as u
from astropy.coordinates import SkyCoord

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

#######################################################

def add_history():
    for file in (glob.glob('*_W_bm_1.0_SC_*.fits')) :
        f = open(parset_file,'r')
        print file
        for line in f:
            if line[0] == "#":
               pass;
            else:
               line = line.split('\n')[0]
               hdulist = pyfits.open(file, mode='update')
               head = hdulist[0].header
               add = line.split('#')[0]
               head['HISTORY'] = add
               hdulist.flush()
               # Add software version numbers
               wsclean_version = commands.getstatusoutput('wsclean -version')[1].split('\n')[1]
               head['HISTORY'] = wsclean_version
               cotter_version = commands.getstatusoutput('cotter -version')[1].split('\n')[0]
               aoflagger_version = commands.getstatusoutput('cotter -version')[1].split('\n')[1]
               head['HISTORY'] = cotter_version
               head['HISTORY'] = aoflagger_version
        hdulist.flush()

####################################################

def run_cotter(obs_id):
    #os.system('make_metafits.py --gps='+str(obs_id))
    os.system('mv '+str(obs_id)+'/*_metafits_ppds.fits .')
    #os.system('cotter -o '+str(obs_id)+'.ms -mem 75 -timeres 2 -freqres 10 -m '+str(obs_id)+'.metafits '+str(obs_id)+'/*.fits') # Frequency resolution 10 KHz 
    os.system('cotter -o '+str(obs_id)+'.ms -mem 75 -timeres 2 -freqres 80 -m '+str(obs_id)+'.metafits '+str(obs_id)+'/*.fits')  # Frequency resolution 80 KHz

####################################################
# Read the location parset to find the paths
locs = read_parset(loc_parset_file)
SIP_home = locs['SIP_home']
error_logs = locs['error_logs']
msgen_loc    = locs['msgen_loc']
results_dir = locs['results_dir']
OBS_ID_LIST = open(SIP_home+'/obs_id_list.txt', 'r')

######## Get the galactic b value ############

def get_b(ms):
        command = 'msinfo '+ms
        term_out=os.popen(command).read()
        s = term_out.split()
        ra_in = s[len(s)-2].split(',')[1]
        dec_in = s[len(s)-3].split('=')[1]
        print 'Observation coordinates:'
        print ra_in, dec_in
        c = SkyCoord(ra=float(ra_in)*u.degree, dec=float(dec_in)*u.degree)
        return c.galactic.b.deg

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

### Get the galactic b-value ###
gal_b = get_b(ms = str(uvfits_dir)+'/'+str(obs_id)+".ms")
print "Galactic b:"
print gal_b
######### Run the CASA pipe ##########
file_to_process = (str(uvfits_dir)+'/'+str(obs_id)+".ms") 
print 'Created '+file_to_process+' : parsing to CASA for reduction' 
os.system("/short/ek6/CASA/casapy-stable-42.0.26465-001-64b/casapy -c "+SIP_home+"/SIP_128T_parallel_phase_3.py  "+file_to_process+' '+cal+' '+str(gal_b))
# Add the parset to the header
add_history()
# Copy all the images to results dir. 
os.system('cp *_I.fits '+results_dir)
os.system('cp *_XX.fits '+results_dir)
os.system('cp *_YY.fits '+results_dir)
os.system('cp *_Q.fits '+results_dir)
os.system('cp *_U.fits '+results_dir)
os.system('cp *_V.fits '+results_dir)
#os.system('cp *-image.fits '+results_dir)
# Remove the raw data (optional see parset)

doRemove = parset['doRemove']
if doRemove:
   os.system('rm -rf '+str(msgen_loc)+'/'+str(obs_id))     
