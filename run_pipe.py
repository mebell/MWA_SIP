################################################################################
# File to create and submit multiple job files for downloading and processing. #
################################################################################

import os, sys
import re

####################################################
#Parset files path(s)
loc_parset_file    = '/Users/bel27a/Work/MWA_SIP/loc_parset.txt'
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
SIP_home= = locs['SIP_home']
error_logs = locs['error_logs']

# Work out which GPS ID / datafile we are going to work on
id_file = open(SIP_home+'/obs_id_list.txt', 'r')

for line in id_file: 
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


