import os, sys
import re

################################################################################
# File to create and submit multiple job files for downloading and processing. #
# This script stages the data reduction so the storage area does not fill up.  # 
################################################################################

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

####################################################

def run_job(id, deps):
    print '#####################################################'
    ### Run the download job on the  "copy" que (see agruments in header of "template_download)
    os.system('cp template_download download.go') # Copy the template jobfile 
    job_file = open('download.go', 'a')
    print 'Writing appropriate download download file for observation ' 
    # Add the appropriate command. 
    job_file.write('python '+SIP_home+'/get_data.py '+id)
    job_file.close()
    ####### Error Logs ########
    name = id.split('/')[-1]        # Define the output and error log names
    name = re.split("[\r\n]+",name)[0] # Get rid of the return carriage
    error_log =  error_logs+'/'+name+'.download.error'
    output_log = error_logs+'/'+name+'.download.output'
       ######## Normal Que  ########
    if len(deps)==0:
       ##############################
       ########## Download ##########       
       print 'Submitting download to qsub NORMAL'
       print 'Download command is = qsub -e '+error_log+' -o '+output_log+' download.go'
       download_command = 'qsub -e '+error_log+' -o '+output_log+' download.go'
       down_out = os.popen(download_command).read()
       down_out = re.split("[\r\n]+",down_out)[0] # Remove return carriage
       #sub_jobs.append(term_out)
       ##############################
       ########## Processing ########
       os.system('cp template_jobfile job_file.go') # Copy the template jobfile 
       job_file = open('job_file.go', 'a')
       print 'Will only exceute qsub job when download is complete'
       # Add the appropriate command.  
       job_file.write('python '+SIP_home+'/pre_proc_pipe.py '+id)
       job_file.close()
       # Submit the file to qsub.
       name = id.split('/')[-1]        # Define the output and error log names
       name = re.split("[\r\n]+",name)[0] # Get rid of the return carriage
       error_log =  error_logs+'/'+name+'.proc.error'
       output_log = error_logs+'/'+name+'.proc.output'
       print 'Data reduction command is = qsub -W depend=afterok:'+down_out+' -e '+error_log+' -o '+output_log+' job_file.go'
       print 'Submitting jobfile'
       proc_command = 'qsub -W depend=afterok:'+down_out+' -e '+error_log+' -o '+output_log+' job_file.go'
       proc_out = os.popen(proc_command).read()
       proc_out = re.split("[\r\n]+",proc_out)[0] # Remove return carriage
       sub_jobs.append(proc_out)
       print '#####################################################'
    #################################
    ######### Dependency Que ########
    dep_string = ''
    if len(deps)>0:
       for k in range(len(deps)):
           dep_string = dep_string + deps[k]
           dep_string = dep_string + ':'    
       ##############################
       ######### Download ########### 
       print 'Submitting download to qsub DEPENDENCY'
       download_command = 'qsub -W depend=afterany:'+dep_string+' -e '+error_log+' -o '+output_log+' download.go'
       print 'Download command is '+download_command
       down_out =os.popen(download_command).read()
       down_out = re.split("[\r\n]+", down_out)[0] # Remove return carriage
       #sub_jobs.append(term_out)
       #############################
       ######## Processing #########
       os.system('cp template_jobfile job_file.go') # Copy the template jobfile 
       job_file = open('job_file.go', 'a')
       print 'Will only exceute qsub job when download is complete' 
       # Add the appropriate command.  
       job_file.write('python '+SIP_home+'/pre_proc_pipe.py '+id)
       job_file.close()
       # Submit the file to qsub.
       name = id.split('/')[-1]        # Define the output and error log names
       name = re.split("[\r\n]+",name)[0] # Get rid of the return carriage
       error_log =  error_logs+'/'+name+'.proc.error'
       output_log = error_logs+'/'+name+'.proc.output'
       print 'Data reduction command is = qsub -W depend=afterok:'+down_out+' -e '+error_log+' -o '+output_log+' job_file.go'
       print 'Submitting jobfile'
       proc_command = 'qsub -W depend=afterok:'+down_out+':'+dep_string+' -e '+error_log+' -o '+output_log+' job_file.go'
       proc_out = os.popen(proc_command).read()
       proc_out = re.split("[\r\n]+",proc_out)[0] # Remove return carriage
       sub_jobs.append(proc_out)
       #os.system('qsub -W depend=afterok:'+term_out+' -e '+error_log+' -o '+output_log+' job_file.go')
       print '#####################################################'
    return sub_jobs

############## Main loop ###############
# Work out which GPS ID / datafile we are going to work on 

id_file = open(SIP_home+'/obs_id_list.txt', 'r')
num_lines = sum(1 for line in open(SIP_home+'/obs_id_list.txt'))
lines=id_file.readlines()

sub_jobs = []
count = 0
step = 60

for start in range(0,num_lines,step):
    stop = start + step
    for k in range(start, stop):
        if k > num_lines:
           pass;
        else:
           if k<=step:
              run_job(lines[k],deps=[])
           if k>step:
              deps_low = start-step 
              deps_high = stop-step-1
              run_job(lines[k],deps=sub_jobs[deps_low:deps_high])

