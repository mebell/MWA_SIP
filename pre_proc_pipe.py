import os
import sys

# A script to run cotter then CASA. This must be in a 
# different script to the download becuase we use different
# ques to submit the qsub commands. Download = copq which uses node
# that can see the outside world, but are limited in number. Normal 
# que which only used compute nodes, with no outside access. 


################ Configs ####################
OBS_ID_LIST = '/home/562/meb562/SIP/obs_id_list.txt' # This contains the GPS IDs of the observations you want to reduce.
UVGEN_LOC    = '/short/ek6/meb562/tmp_data/'
results_dir='/short/ek6/meb562/SIP_results/test'
##############################################

def run_cotter(obs_id):
    #os.system('make_metafits.py --gps='+str(obs_id))
    os.system('cotter -o '+str(obs_id)+'.ms -mem 75 -timeavg 2 -freqavg 4 -m '+str(obs_id)+'.metafits '+str(obs_id)+'/*.fits')
    #os.system('cotter -o '+str(obs_id)+'.ms -mem 75 -timeavg 1 -freqavg 1 -m '+str(obs_id)+'.metafits '+str(obs_id)+'/*.fits')

############## Main code ######################

obs_id = sys.argv[1] # Get the obs_id we want to work on. Parsed to the script by run_pipe.py

os.chdir(UVGEN_LOC)
os.chdir(obs_id)

if os.path.exists(str(obs_id)+'.ms'):
   print 'Data already pre-processed, skipping'
else:    
   run_cotter(obs_id)

uvfits_dir = os.getcwd()
######### Run the CASA pipe ##########
#os.system('change_db.py curtin')
file_to_process = (str(uvfits_dir)+'/'+str(obs_id)+".ms") 
print 'Created '+file_to_process+' : parsing to CASA for reduction' 
os.system("/short/ek6/CASA/casapy-stable-42.0.26465-001-64b/casapy -c /home/562/meb562/SIP/SIP_128T_parallel_phase_2.py  "+file_to_process)
# Run make_beam.py outside of casa becuase pyephem fails to compile with casa 4.2 THIS IS A PAIN IN THE ARSE!!!!!
f = open('delays.txt')
lines = f.readlines()
str_delays = lines[0]
f.close()
outimage = obs_id+'_XX.fits'
os.system('python /short/ek6/MWA_Code/bin/make_beam.py -f '+outimage+' -d '+str_delays) # Make the beam files
XX_beam = obs_id+'_XX_beamXX.fits'
YY_beam = obs_id+'_XX_beamYY.fits'
XX_image = obs_id+'_XX.fits'
YY_image = obs_id+'_YY.fits'
os.system('/short/ek6/CASA/casapy-stable-42.0.26465-001-64b/casapy -c /home/562/meb562/SIP/make_casa_stoke_I.py '+str(obs_id)+' '+str(XX_image)+' '+str(YY_image)+' '+str(XX_beam)+' '+str(YY_beam))
os.system('cp *_I.fits '+results_dir)
os.system('cp *XX-image* '+results_dir)
os.system('cp *YY-image* '+results_dir)
os.system('cp *image-* '+results_dir)
# Remove the raw data, may want to turn this off. 
#os.system('rm -rf '+str(UVGEN_LOC)+'/'+str(obs_id))     
