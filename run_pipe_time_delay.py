################################################################################
# File to create and submit multiple job files for downloading and processing. #
################################################################################

import os, sys
import re
import time
import glob
from time import gmtime, strftime


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

def check_done(obs_id):
    results_dir = '/short/ek6/meb562/SIP_results/MWA_SIP_out/'
    os.chdir(results_dir)
    obs_id = obs_id.split('\n')[0]
    n_files = len(glob.glob('*'+obs_id+'*'))
    if n_files > 0:
       return True
    else:
       return False

def check_dir_made(obs_id):
    tmp_dir = "/short/ek6/meb562/tmp_data"
    os.chdir(tmp_dir)
    obs_id = obs_id.split('\n')[0]
    if os.path.exists(obs_id) == True:
       return True
       print "true"
    else: 
       return False

def submit_job(line):
    os.chdir('/home/562/meb562/MWA_SIP/')
    ### Run the download job on the  "copy" que (see agruments in header of "template_download)
    os.system('cp template_download download.go') # Copy the template jobfile 
    job_file = open('download.go', 'a')
    print 'Writing appropriate download job file for observation '+line 
    # Add the appropriate command. 
    job_file.write('python '+SIP_home+'/get_data.py '+line)
    job_file.close()
    # Submit the file to qsub.
    name = line.split('/')[-1]        # Define the output and error log names
    name = re.split("[\r\n]+",name)[0] # Get rid of the return carriage
    error_log  = error_logs+'/'+name+'.download.error'
    output_log = error_logs+'/'+name+'.download.output'
    print 'Qsub command is = qsub -e '+error_log+' -o '+output_log+' download.go'
    download_command = 'qsub -e '+error_log+' -o '+output_log+' download.go'
    term_out=os.popen(download_command).read()
    term_out = re.split("[\r\n]+",term_out)[0] # Remove return carriage
    ### Run the processing on the "normal" que (see agruments in header of "template_jobfile)
    os.system('cp template_jobfile job_file.go') # Copy the template jobfile 
    job_file = open('job_file.go', 'a')
    print 'Writing appropriate job file for observation '+line
    print 'Will only exceute qsub job when download is complete' 
    # Add the appropriate command.  
    job_file.write('python '+SIP_home+'/pre_proc_pipe.py '+line)
    job_file.close()
    # Submit the file to qsub.
    name = line.split('/')[-1]        # Define the output and error log names
    name = re.split("[\r\n]+",name)[0] # Get rid of the return carriage
    error_log  = error_logs+'/'+name+'.proc.error'
    output_log = error_logs+'/'+name+'.proc.output'
    print 'Qsub command is = qsub -W depend=afterok:'+term_out+' -e '+error_log+' -o '+output_log+' job_file.go'
    os.system('qsub -W depend=afterok:'+term_out+' -e '+error_log+' -o '+output_log+' job_file.go')

####################################################
# Read the location parset to find the paths
locs = read_parset(loc_parset_file)
SIP_home   = locs['SIP_home']
error_logs = locs['error_logs']

####################################################

# Work out which GPS ID / datafile we are going to work on
id_file = open(SIP_home+'/obs_id_list.txt', 'r')

n = 0
for line in id_file:
     q_status = os.popen("qstat -u meb562 | grep job_file.g | wc").read()
     n_jobs = q_status.split()[0]
     print "File number "+str(n)+ ", n_jobs "+str(n_jobs)
     while float(n_jobs) > 22:
         time.sleep(10)
         print "Waiting for queue to clear, "+str(n_jobs)+" jobs running"
         q_status = os.popen("qstat -u meb562 | grep job_file.g | wc").read()
         n_jobs = q_status.split()[0]
     if (check_done(line) == False) and (check_dir_made(line) == False):
             print "Submitting jobs"
             submit_job(line)
             n +=1
     else:
             print "Job already processed or in queue, skipping"
             n +=1


